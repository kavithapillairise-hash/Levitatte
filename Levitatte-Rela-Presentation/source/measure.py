"""
Exact text measurement for the deck layout.

The first version of the deck guessed line counts from an average-character-width constant.
That is unreliable: ragged-right wrapping in a narrow column wastes 10 to 15 per cent of the
measured width, so blocks silently overlapped and two shapes were even emitted with negative
height, which LibreOffice renders in the wrong place entirely.

This module measures against the real font files instead, so every block height in deck.py is
derived rather than estimated. Sizes are handled in points and PIL is given the point size as a
pixel size, which makes one returned pixel exactly one point.
"""
import os
import re

from PIL import ImageFont

FONT_DIR = os.path.expanduser("~/Library/Fonts")

FILES = {
    ("Inter", False, False): "Inter-Regular.otf",
    ("Inter", True, False): "Inter-SemiBold.otf",
    ("Inter", False, True): "Inter-Italic.otf",
    ("Inter", True, True): "Inter-SemiBoldItalic.otf",
    ("Playfair Display", False, False): "PlayfairDisplayStatic-Regular.ttf",
    ("Playfair Display", True, False): "PlayfairDisplayStatic-Bold.ttf",
    ("Playfair Display", False, True): "PlayfairDisplay-Italic[wght].ttf",
    ("Playfair Display", True, True): "PlayfairDisplay-Italic[wght].ttf",
}

_CACHE = {}


def font(name="Inter", size=9.0, bold=False, italic=False):
    key = (name, round(size, 2), bold, italic)
    if key not in _CACHE:
        fn = FILES.get((name, bold, italic))
        if fn is None:
            raise KeyError(f"no font file mapped for {(name, bold, italic)}")
        path = os.path.join(FONT_DIR, fn)
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        # PIL wants an integer-ish pixel size; keep the fractional size, it accepts floats
        _CACHE[key] = ImageFont.truetype(path, size)
    return _CACHE[key]


def natural(name="Inter", bold=False, italic=False):
    """The font's own single-line height as a multiple of the point size.

    OOXML line spacing is a PERCENTAGE OF THIS, not of the point size, so a block's real
    height is size x natural x spacing. Inter is 1.22 and Playfair Display 1.35, which is
    exactly how much the first version of the deck undersized every text block by.
    """
    f = font(name, 100.0, bold, italic)
    a, d = f.getmetrics()
    return (a + d) / 100.0


def spacing_pct(lead, name="Inter", bold=False, italic=False):
    """Convert an absolute leading (multiple of point size) to an OOXML spacing multiple."""
    return lead / natural(name, bold, italic)


def text_pt(text, size=9.0, name="Inter", bold=False, italic=False, track=0.0):
    """Advance width of `text` in points. `track` is per-character spacing in points."""
    if not text:
        return 0.0
    f = font(name, size, bold, italic)
    return f.getlength(text) + track * len(text)


SAFETY_PT = 0.75   # absorbs small kerning differences against the real renderer


def _tokens(runs):
    """Flatten runs into [(kind, text, width_pt)] where kind is 'word' or 'glue'.

    Whitespace is measured rather than normalised. Collapsing it with str.split() is what made
    a mixed-format line measure ~7pt narrower than the renderer drew it, because the deliberate
    double-space between a label and its body text simply vanished.
    """
    out = []
    for text, size, name, bold, italic, track in runs:
        for part in re.split(r"(\s+)", text):
            if not part:
                continue
            kind = "glue" if part.isspace() else "word"
            out.append((kind, part, text_pt(part, size, name, bold, italic, track)))
    return out


def _wrap_tokens(toks, width_in):
    """Greedy line breaking over measured tokens. Returns a list of line widths in points."""
    limit = width_in * 72.0 - SAFETY_PT
    widths, cur, pending = [], 0.0, 0.0
    for kind, _part, w in toks:
        if kind == "glue":
            if cur > 0:
                pending += w
            continue
        if cur > 0 and cur + pending + w > limit:
            widths.append(cur)
            cur, pending = w, 0.0
        else:
            cur += pending + w
            pending = 0.0
    widths.append(cur)
    return widths


def wrap(text, width_in, size=9.0, name="Inter", bold=False, italic=False, track=0.0):
    """Greedy word wrap. Returns the list of lines that will be laid out."""
    limit = width_in * 72.0 - SAFETY_PT
    words = text.split()
    if not words:
        return [""]
    lines, cur = [], words[0]
    for w in words[1:]:
        trial = cur + " " + w
        if text_pt(trial, size, name, bold, italic, track) <= limit:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def nlines(text, width_in, size=9.0, name="Inter", bold=False, italic=False, track=0.0):
    """Line count, measuring whitespace exactly rather than normalising it."""
    return len(_wrap_tokens(_tokens([(text, size, name, bold, italic, track)]), width_in))


def height_in(text, width_in, size=9.0, name="Inter", bold=False, italic=False,
              track=0.0, lead=1.34, pad=0.03):
    """Height in inches a wrapped block needs, including a small safety pad.

    `lead` is ABSOLUTE: a multiple of the point size, the same number handed to
    spacing_pct() when the paragraph is written, so the two cannot disagree.
    """
    n = nlines(text, width_in, size, name, bold, italic, track)
    return n * size * lead / 72.0 + pad


def wrap_runs(runs, width_in):
    """Line count for a mixed-formatting paragraph.

    `runs` is a list of (text, size, name, bold, italic, track). Needed because a line that
    starts with a bold, letter-spaced label and continues in regular body text is wider than
    the same string measured as plain text, which is exactly how the measurement column on
    slide 4 came to overlap itself.
    """
    return len(_wrap_tokens(_tokens(runs), width_in))


def height_runs(runs, width_in, lead=1.34, pad=0.03):
    n = wrap_runs(runs, width_in)
    size = max(r[1] for r in runs)
    return n * size * lead / 72.0 + pad


def fits(text, width_in, size=9.0, **kw):
    """True when the string lays out on a single line."""
    return nlines(text, width_in, size, **kw) == 1


def shrink_to_fit(text, width_in, start=9.0, floor=5.6, step=0.1, lines=1, **kw):
    """Largest size at or below `start` that lays `text` out in `lines` lines or fewer."""
    size = start
    while size > floor and nlines(text, width_in, size, **kw) > lines:
        size -= step
    return round(size, 2)
