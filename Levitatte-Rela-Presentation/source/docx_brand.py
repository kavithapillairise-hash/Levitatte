"""
Levitatte Learning & Development — proposal renderer.
Light (ivory + antique gold + graphite) theme, matching the Levitatte light deck palette.
Reads copy.json  ->  writes Levitatte-Rela-Hospital-LD-Proposal.docx
"""
import json
import os
import sys

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Emu, Inches, Pt, RGBColor

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = "/private/tmp/claude-502/-Users-adityalakshmipathy-Documents-Transcripta/dc4bb950-0959-40fd-b54f-09505582fb0d/scratchpad"
OWL = os.path.join(HERE, "owl_refined.png")

# ── Light-theme palette (lifted verbatim from the Levitatte light deck) ──────────
INK      = RGBColor(0x20, 0x1C, 0x15)   # near-black headings
BODY     = RGBColor(0x55, 0x51, 0x49)   # warm dark-grey body
MUTE     = RGBColor(0x8A, 0x86, 0x7C)
FAINT    = RGBColor(0xB1, 0xAC, 0xA1)
GOLD     = RGBColor(0x93, 0x74, 0x25)   # deep antique gold — labels & rules
GOLD_L   = RGBColor(0xB0, 0x89, 0x30)   # richer gold — display numerals
TAGCOL   = RGBColor(0x4A, 0x42, 0x33)

PAGE_BG  = "FAF8F3"   # warm ivory paper
LINE_HEX = "DDD7C8"   # hairline
CARD_HEX = "FCF8EF"   # featured / callout card
HEAD_HEX = "F1EDE2"   # table header band
ZEBRA_HEX = "FCFAF5"  # table zebra

DISP = "Playfair Display"
SANS = "Inter"

BULLET = "–"     # en dash bullet, set in gold


# ── low-level XML helpers ───────────────────────────────────────────────────────
def _el(tag, **attrs):
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn("w:" + k), str(v))
    return e


def font(run, name=SANS, size=10.5, color=BODY, bold=False, italic=False,
         caps=False, track=None):
    """Set a run's typography. `track` = character spacing in twentieths of a point."""
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = _el("w:rFonts")
        rpr.insert(0, rf)
    for a in ("ascii", "hAnsi", "cs", "eastAsia"):
        rf.set(qn("w:" + a), name)
    if caps:
        rpr.append(_el("w:caps", val="1"))
    if track:
        rpr.append(_el("w:spacing", val=int(track)))
    return run


def spacing(p, before=0, after=6, line=None):
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    if line:
        pf.line_spacing = line
    return p


def keep_with_next(p):
    p.paragraph_format.keep_with_next = True
    return p


def para_border(p, side="left", color="937425", size=18, space=10):
    """Coloured rule on one side of a paragraph. size is in eighths of a point."""
    ppr = p._element.get_or_add_pPr()
    bdr = ppr.find(qn("w:pBdr"))
    if bdr is None:
        bdr = _el("w:pBdr")
        ppr.append(bdr)
    bdr.append(_el("w:" + side, val="single", sz=size, space=space, color=color))
    return p


def shade(obj, hex_fill):
    """Shade a paragraph or a table cell."""
    pr = obj._element.get_or_add_pPr() if hasattr(obj, "paragraph_format") else obj._element.get_or_add_tcPr()
    pr.append(_el("w:shd", val="clear", color="auto", fill=hex_fill))
    return obj


def cell_margins(cell, top=90, bottom=90, left=130, right=130):
    tcpr = cell._element.get_or_add_tcPr()
    mar = _el("w:tcMar")
    for tag, v in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        mar.append(_el("w:" + tag, w=v, type="dxa"))
    tcpr.append(mar)


def table_hairlines(table, color=LINE_HEX, inner_h=True, inner_v=False, box=False):
    tblpr = table._element.tblPr
    borders = _el("w:tblBorders")
    spec = {
        "top": box, "left": False, "bottom": box, "right": False,
        "insideH": inner_h, "insideV": inner_v,
    }
    for tag, on in spec.items():
        borders.append(
            _el("w:" + tag, val="single" if on else "none", sz=6, space=0, color=color)
        )
    tblpr.append(borders)


def no_autofit(table, widths):
    """Pin column widths (list of Inches).

    Setting only the cell widths is not enough: LibreOffice and Word both resolve column
    geometry from w:tblGrid, which python-docx creates with equal columns. The grid has to be
    rewritten too, or every table renders as equal fractions regardless of the cell widths.
    """
    table.autofit = False
    tblpr = table._element.tblPr
    tblpr.append(_el("w:tblLayout", type="fixed"))

    grid = table._element.find(qn("w:tblGrid"))
    if grid is not None:
        table._element.remove(grid)
    grid = _el("w:tblGrid")
    for w in widths:
        grid.append(_el("w:gridCol", w=int(w.inches * 1440)))
    # w:tblGrid must sit immediately after w:tblPr
    tblpr.addnext(grid)

    for row in table.rows:
        for i, w in enumerate(widths):
            if i < len(row.cells):
                row.cells[i].width = w


def hairline(doc, color="937425", size=12, before=4, after=14, width=None):
    p = doc.add_paragraph()
    spacing(p, before=before, after=after)
    if width:
        p.paragraph_format.right_indent = width
    para_border(p, "bottom", color=color, size=size, space=0)
    r = p.add_run("")
    font(r, SANS, 1, INK)
    return p


def page_break(doc):
    p = doc.add_paragraph()
    spacing(p, 0, 0)
    p.add_run().add_break(WD_BREAK.PAGE)
    return p


# ── document chrome ─────────────────────────────────────────────────────────────
def set_page_background(doc, hex_color=PAGE_BG):
    bg = _el("w:background", color=hex_color)
    doc.element.insert(0, bg)
    doc.settings.element.append(_el("w:displayBackgroundShape"))


def setup_section(sec, first_page_footer=False):
    sec.page_width, sec.page_height = Inches(8.27), Inches(11.69)   # A4
    sec.left_margin = Inches(0.95)
    sec.right_margin = Inches(0.95)
    sec.top_margin = Inches(0.85)
    sec.bottom_margin = Inches(0.8)
    sec.footer_distance = Inches(0.45)
    sec.different_first_page_header_footer = first_page_footer


def add_page_field(paragraph):
    r = paragraph.add_run()
    fld = _el("w:fldChar", fldCharType="begin")
    r._element.append(fld)
    r2 = paragraph.add_run()
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"
    r2._element.append(instr)
    r3 = paragraph.add_run()
    r3._element.append(_el("w:fldChar", fldCharType="end"))
    for rr in (r, r2, r3):
        font(rr, SANS, 7.5, MUTE)


def build_footer(sec, left_text):
    f = sec.footer
    p = f.paragraphs[0]
    p.text = ""
    spacing(p, before=0, after=0)
    para_border(p, "top", color=LINE_HEX, size=6, space=8)
    tabs = p.paragraph_format.tab_stops
    tabs.add_tab_stop(Inches(6.37), WD_TAB_ALIGNMENT.RIGHT)
    font(p.add_run(left_text), SANS, 7.5, MUTE, track=4)
    p.add_run("\t")
    add_page_field(p)


# ── cover ───────────────────────────────────────────────────────────────────────
def build_cover(doc, meta):
    # owl mark
    if os.path.exists(OWL):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        spacing(p, before=40, after=2)
        p.add_run().add_picture(OWL, width=Inches(2.25))

    # wordmark
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    spacing(p, before=0, after=2)
    font(p.add_run("LEVITATTE"), DISP, 27, INK, bold=True, track=118)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    spacing(p, before=0, after=20)
    font(p.add_run("LEARNING  &  DEVELOPMENT"), SANS, 8, GOLD, bold=True, track=58)

    # centred gold hairline
    p = doc.add_paragraph()
    spacing(p, before=0, after=24)
    p.paragraph_format.left_indent = Inches(2.79)
    p.paragraph_format.right_indent = Inches(2.79)
    para_border(p, "bottom", color="B08930", size=10, space=0)
    font(p.add_run(""), SANS, 1, INK)

    # eyebrow
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    spacing(p, before=0, after=12)
    font(p.add_run(meta["eyebrow"]), SANS, 8.5, GOLD, bold=True, track=62)

    # title
    for line in meta["title_lines"]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        spacing(p, before=0, after=4, line=1.12)
        font(p.add_run(line), DISP, 25, INK, bold=True)

    # subtitle
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    spacing(p, before=14, after=10, line=1.35)
    font(p.add_run(meta["subtitle"]), DISP, 12.5, TAGCOL, italic=True)

    if meta.get("descriptor"):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        spacing(p, before=0, after=26, line=1.45)
        p.paragraph_format.left_indent = Inches(0.75)
        p.paragraph_format.right_indent = Inches(0.75)
        font(p.add_run(meta["descriptor"]), SANS, 7.5, GOLD, bold=True, track=34)

    # prepared-for card
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = t.cell(0, 0)
    shade(c, CARD_HEX)
    cell_margins(c, top=250, bottom=250, left=260, right=260)
    table_hairlines(t, color="E2DBCA", inner_h=False, box=True)
    no_autofit(t, [Inches(5.1)])

    q = c.paragraphs[0]
    q.alignment = WD_ALIGN_PARAGRAPH.CENTER
    spacing(q, 0, 5)
    font(q.add_run("PREPARED FOR"), SANS, 7.5, MUTE, bold=True, track=58)

    q = c.add_paragraph()
    q.alignment = WD_ALIGN_PARAGRAPH.CENTER
    spacing(q, 0, 3, line=1.2)
    font(q.add_run(meta["client"]), DISP, 15, INK, bold=True)

    q = c.add_paragraph()
    q.alignment = WD_ALIGN_PARAGRAPH.CENTER
    spacing(q, 0, 0)
    font(q.add_run(meta["client_sub"]), SANS, 9, BODY)

    # footer block
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    spacing(p, before=34, after=3)
    font(p.add_run(meta["date"]), SANS, 8.5, MUTE, bold=True, track=40)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    spacing(p, before=0, after=0, line=1.4)
    font(p.add_run(meta["confidential"]), SANS, 7.5, FAINT, italic=True)

    # anchor the lower third with the contact line
    p = doc.add_paragraph()
    spacing(p, before=26, after=8)
    p.paragraph_format.left_indent = Inches(2.29)
    p.paragraph_format.right_indent = Inches(2.29)
    para_border(p, "bottom", color=LINE_HEX, size=6, space=0)
    font(p.add_run(""), SANS, 1, INK)

    lines = meta["contact_line"]
    if isinstance(lines, str):
        lines = [lines]
    for i, ln in enumerate(lines):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        spacing(p, before=0, after=3 if i < len(lines) - 1 else 0, line=1.4)
        font(p.add_run(ln), SANS, 7.5, MUTE if i == 0 else FAINT, track=16)


def build_contents(doc, sections):
    eyebrow_title(doc, "CONTENTS", "What This Document Covers", number=None)
    n = 0
    for s in sections:
        n += 1
        p = doc.add_paragraph()
        spacing(p, before=0, after=7)
        tabs = p.paragraph_format.tab_stops
        tabs.add_tab_stop(Inches(6.37), WD_TAB_ALIGNMENT.RIGHT)
        font(p.add_run(f"{n:02d}"), DISP, 10.5, GOLD_L, bold=True)
        font(p.add_run("   "), SANS, 10.5, INK)
        font(p.add_run(s["title"]), SANS, 10.5, INK)
        if s.get("eyebrow"):
            p.add_run("\t")
            font(p.add_run(s["eyebrow"].upper()), SANS, 7.5, MUTE, track=25)


# ── section rendering ───────────────────────────────────────────────────────────
def eyebrow_title(doc, eyebrow, title, number=None):
    if eyebrow:
        p = doc.add_paragraph()
        spacing(p, before=0, after=6)
        keep_with_next(p)
        if number:
            font(p.add_run(f"{number:02d}   "), DISP, 9.5, GOLD_L, bold=True)
        font(p.add_run(eyebrow.upper()), SANS, 8, GOLD, bold=True, track=58)

    p = doc.add_paragraph()
    spacing(p, before=0, after=8, line=1.15)
    keep_with_next(p)
    font(p.add_run(title), DISP, 20, INK, bold=True)

    q = doc.add_paragraph()
    spacing(q, before=0, after=13)
    keep_with_next(q)
    para_border(q, "bottom", color="937425", size=10, space=0)
    q.paragraph_format.right_indent = Inches(4.55)
    font(q.add_run(""), SANS, 1, INK)


def render_para(doc, text, size=10.5, color=BODY, after=9, italic=False, bold=False,
                first=False):
    p = doc.add_paragraph()
    spacing(p, before=0, after=after, line=1.42)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if first:
        font(p.add_run(text), SANS, 11.5, TAGCOL, italic=False)
    else:
        font(p.add_run(text), SANS, size, color, italic=italic, bold=bold)
    return p


def render_subhead(doc, text):
    p = doc.add_paragraph()
    spacing(p, before=13, after=6)
    keep_with_next(p)
    font(p.add_run(text), DISP, 12.5, INK, bold=True)
    return p


def render_bullets(doc, items, numbered=False):
    for i, it in enumerate(items, 1):
        p = doc.add_paragraph()
        spacing(p, before=0, after=5, line=1.36)
        pf = p.paragraph_format
        pf.left_indent = Inches(0.32)
        pf.first_line_indent = Inches(-0.32)
        pf.tab_stops.add_tab_stop(Inches(0.32), WD_TAB_ALIGNMENT.LEFT)
        if numbered:
            font(p.add_run(f"{i:02d}"), DISP, 10, GOLD_L, bold=True)
        else:
            font(p.add_run(BULLET), SANS, 10.5, GOLD_L, bold=True)
        font(p.add_run("\t"), SANS, 10.5, BODY)
        # bold a leading "Label:" or "Label —" if present
        head, sep, tail = it.partition(": ")
        if sep and len(head) <= 58:
            font(p.add_run(head + ":"), SANS, 10.5, INK, bold=True)
            font(p.add_run(" " + tail), SANS, 10.5, BODY)
        else:
            font(p.add_run(it), SANS, 10.5, BODY)


def render_table(doc, columns, rows):
    t = doc.add_table(rows=1, cols=len(columns))
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    table_hairlines(t, inner_h=True, inner_v=False, box=False)

    # sensible widths: first column wider, a narrow trailing numeric column
    total = 6.37
    n = len(columns)
    if n == 2:
        widths = [Inches(4.25), Inches(2.12)]
    elif n == 3:
        last = columns[-1].strip().lower()
        if last in ("sessions", "value", "when", "reported"):
            widths = [Inches(2.15), Inches(3.22), Inches(1.00)]
        else:
            widths = [Inches(1.95), Inches(2.72), Inches(1.70)]
    elif n == 4:
        widths = [Inches(1.15), Inches(2.35), Inches(1.62), Inches(1.25)]
    else:
        widths = [Inches(total / n)] * n

    hdr = t.rows[0]
    for i, ctext in enumerate(columns):
        c = hdr.cells[i]
        shade(c, HEAD_HEX)
        cell_margins(c, top=95, bottom=95, left=120, right=120)
        p = c.paragraphs[0]
        spacing(p, 0, 0)
        font(p.add_run(ctext.upper()), SANS, 7.5, GOLD, bold=True, track=34)

    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        is_total = str(row[0]).strip().lower() in ("total", "totals")
        for i, val in enumerate(row[: len(columns)]):
            c = cells[i]
            cell_margins(c, top=85, bottom=85, left=120, right=120)
            if is_total:
                shade(c, HEAD_HEX)
            elif ri % 2 == 1:
                shade(c, ZEBRA_HEX)
            p = c.paragraphs[0]
            spacing(p, 0, 0, line=1.26)
            first_col = i == 0
            font(
                p.add_run(str(val)),
                SANS,
                9,
                INK if (first_col or is_total) else BODY,
                bold=is_total or first_col,
            )
    no_autofit(t, widths)

    tail = doc.add_paragraph()
    spacing(tail, before=0, after=9)
    font(tail.add_run(""), SANS, 1, INK)
    return t


def render_kv(doc, rows):
    t = doc.add_table(rows=0, cols=2)
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    table_hairlines(t, inner_h=True, inner_v=False, box=False)
    for ri, row in enumerate(rows):
        label = str(row[0]) if len(row) > 0 else ""
        value = str(row[1]) if len(row) > 1 else ""
        cells = t.add_row().cells
        for i, c in enumerate(cells):
            cell_margins(c, top=90, bottom=90, left=0 if i == 0 else 120, right=120)
            if ri % 2 == 1:
                shade(c, ZEBRA_HEX)
        p = cells[0].paragraphs[0]
        spacing(p, 0, 0, line=1.24)
        font(p.add_run(label.upper()), SANS, 7.5, MUTE, bold=True, track=30)
        p = cells[1].paragraphs[0]
        spacing(p, 0, 0, line=1.28)
        font(p.add_run(value), SANS, 10, INK)
    no_autofit(t, [Inches(2.30), Inches(4.07)])
    tail = doc.add_paragraph()
    spacing(tail, before=0, after=9)
    font(tail.add_run(""), SANS, 1, INK)
    return t


def render_pullquote(doc, text):
    p = doc.add_paragraph()
    spacing(p, before=12, after=13, line=1.34)
    p.paragraph_format.left_indent = Inches(0.22)
    para_border(p, "left", color="B08930", size=20, space=12)
    font(p.add_run(text), DISP, 13.5, TAGCOL, italic=True)
    return p


def render_callout(doc, text):
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    c = t.cell(0, 0)
    shade(c, CARD_HEX)
    cell_margins(c, top=180, bottom=180, left=190, right=190)
    table_hairlines(t, color="E2DBCA", inner_h=False, box=True)
    no_autofit(t, [Inches(6.37)])
    p = c.paragraphs[0]
    spacing(p, 0, 0, line=1.38)
    font(p.add_run("NOTE   "), SANS, 7.5, GOLD, bold=True, track=40)
    font(p.add_run(text), SANS, 9.5, BODY, italic=True)
    tail = doc.add_paragraph()
    spacing(tail, before=0, after=10)
    font(tail.add_run(""), SANS, 1, INK)
    return t


def render_section(doc, sec, number):
    eyebrow_title(doc, sec.get("eyebrow", ""), sec["title"], number=number)
    if sec.get("intro"):
        render_para(doc, sec["intro"], first=True, after=11)

    for b in sec.get("blocks", []):
        kind = b.get("type")
        if kind == "para":
            if b.get("text"):
                render_para(doc, b["text"])
        elif kind == "subhead":
            if b.get("text"):
                render_subhead(doc, b["text"])
        elif kind == "bullets":
            render_bullets(doc, b.get("items") or [])
        elif kind == "numbered":
            render_bullets(doc, b.get("items") or [], numbered=True)
        elif kind == "table":
            cols = b.get("columns") or []
            rws = b.get("rows") or []
            if cols and rws:
                render_table(doc, cols, rws)
        elif kind == "kv":
            if b.get("rows"):
                render_kv(doc, b["rows"])
        elif kind == "pullquote":
            if b.get("text"):
                render_pullquote(doc, b["text"])
        elif kind == "callout":
            if b.get("text"):
                render_callout(doc, b["text"])


# ── main ────────────────────────────────────────────────────────────────────────
def main():
    copy_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "copy.json")
    out_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "proposal.docx")

    with open(copy_path) as fh:
        data = json.load(fh)
    meta = data["meta"]
    sections = data["sections"]

    doc = Document()
    set_page_background(doc)

    # kill default style inheritance surprises
    normal = doc.styles["Normal"]
    normal.font.name = SANS
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = BODY
    normal.paragraph_format.space_after = Pt(0)
    normal.paragraph_format.widow_control = True

    sec = doc.sections[0]
    setup_section(sec, first_page_footer=True)
    # blank first-page footer, real footer from page 2
    sec.first_page_footer.paragraphs[0].text = ""
    build_footer(sec, meta["footer"])

    build_cover(doc, meta)

    page_break(doc)
    build_contents(doc, sections)

    for i, s in enumerate(sections, 1):
        page_break(doc)
        render_section(doc, s, i)

    doc.save(out_path)
    print(f"wrote {out_path}  ({len(sections)} sections)")


if __name__ == "__main__":
    main()
