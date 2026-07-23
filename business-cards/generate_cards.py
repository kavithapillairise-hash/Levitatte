#!/usr/bin/env python3
"""
Levitatte visiting-card generator.

Produces 6 design versions (front + back) as print-ready vector SVGs.

Print geometry (all cards):
  Trim size : 3.5in x 2.0in  (standard business card, 88.9 x 50.8 mm)
  Bleed     : 0.125in (3.175 mm) on every side  -> canvas 3.75in x 2.25in
  Safe area : 0.125in inside the trim (keep all text/logos inside)

Units: SVG viewBox is in points (72 pt = 1 in).
  Canvas (bleed) : 270 x 162
  Trim rectangle : (9, 9)  ->  252 x 144
  Safe rectangle : (18,18) ->  234 x 126

The <svg> width/height are set in inches so a renderer (rsvg-convert) emits a
PDF page at exact physical size. Logos are embedded as base64 so each SVG is a
single self-contained file the printer can use directly.
"""
import base64, html, os, pathlib

HERE = pathlib.Path(__file__).parent
ASSETS = HERE / "assets"
OUT = HERE / "svg"
OUT.mkdir(exist_ok=True)

# ---- brand ---------------------------------------------------------------
GOLD, GOLD_L, GOLD_D = "#c9a84c", "#d4b96a", "#a88a3a"
INK, DARK, CHAR = "#111111", "#1a1a1a", "#2d2d2d"
PAPER, WHITE = "#f5f5f3", "#ffffff"
SILVER, GRAY_L, INK2 = "#b8b8b8", "#8a8a8a", "#333333"

FONT_S = "Inter"          # sans (body / caps)
FONT_D = "Playfair Display"  # display serif (names / taglines)

INFO = dict(
    name="Kavitha Pillai",
    role="Managing Director  &  Head of Training",
    phone="+91 7411 099 183",
    email="kavitha.pillai@levitatte.com",
    web="www.levitatte.com",
    loc="Bengaluru, Karnataka, India",
    brand="LEVITATTE",
    sub="LEARNING  &  DEVELOPMENT",
    tag="Empowering Individuals. Transforming Organizations.",
)

# ---- geometry ------------------------------------------------------------
W, H = 270, 162          # canvas (bleed box)
CX = W / 2

def b64(name):
    return base64.b64encode((ASSETS / name).read_bytes()).decode()

OWL = b64("owl-mark.png");       OWL_AR = 1366 / 932     # w/h
LOCK = b64("logo-lockup.png");   LOCK_AR = 1392 / 1313
FACE = b64("founder-circle.png"); FACE_AR = 1.0

def esc(s):
    return html.escape(str(s), quote=True)

def txt(x, y, s, *, size, fill, family=FONT_S, weight=400, ls=0,
        anchor="start", italic=False, opacity=1.0):
    style = (f"font-family:'{family}';font-size:{size}px;font-weight:{weight};"
             f"fill:{fill};letter-spacing:{ls}px;")
    if italic:
        style += "font-style:italic;"
    if opacity != 1.0:
        style += f"fill-opacity:{opacity};"
    return f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}" style="{style}">{esc(s)}</text>'

def image(data, x, y, w, ar, opacity=1.0):
    h = w / ar
    op = f' opacity="{opacity}"' if opacity != 1.0 else ""
    return (f'<image x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}"'
            f' preserveAspectRatio="xMidYMid meet"{op}'
            f' xlink:href="data:image/png;base64,{data}"/>'), h

# small stroked icons (24x24 source viewBox)
ICONS = dict(
    mail="M2 5.2h20v13.6H2zM2 5.6 12 13 22 5.6",
    phone=("M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6"
           "A19.8 19.8 0 0 1 2.12 4.2 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81"
           "a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45"
           "c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"),
    globe="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zM2 12h20M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20z",
    pin="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0zM12 13a3 3 0 1 0 0-6 3 3 0 0 0 0 6z",
)

def icon(name, x, y, s, color, sw=1.7):
    return (f'<g transform="translate({x:.2f},{y:.2f}) scale({s/24:.4f})" '
            f'fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="{ICONS[name]}"/></g>')

DEFS = f'''<defs>
  <linearGradient id="silver" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f4f4f2"/><stop offset="0.42" stop-color="#cfcfcf"/>
    <stop offset="0.58" stop-color="#b3b3b3"/><stop offset="1" stop-color="#7f7f7f"/>
  </linearGradient>
  <linearGradient id="silverD" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#5a5a5a"/><stop offset="0.5" stop-color="#3c3c3c"/>
    <stop offset="1" stop-color="#242424"/>
  </linearGradient>
  <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{GOLD_L}"/><stop offset="0.5" stop-color="{GOLD}"/>
    <stop offset="1" stop-color="{GOLD_D}"/>
  </linearGradient>
  <radialGradient id="glow" cx="0.5" cy="0.34" r="0.75">
    <stop offset="0" stop-color="{GOLD}" stop-opacity="0.16"/>
    <stop offset="0.55" stop-color="{GOLD}" stop-opacity="0.04"/>
    <stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="goldbar" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{GOLD_L}"/><stop offset="1" stop-color="{GOLD_D}"/>
  </linearGradient>
</defs>'''

def svg(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="3.75in" height="2.25in" viewBox="0 0 {W} {H}">\n{DEFS}\n{body}\n</svg>\n')

def bg(color):
    return f'<rect x="0" y="0" width="{W}" height="{H}" fill="{color}"/>'

def wordmark(cx, y, size, fill="url(#silver)", ls=None):
    if ls is None:
        ls = size * 0.16
    return txt(cx, y, INFO["brand"], size=size, fill=fill, weight=800,
               ls=ls, anchor="middle")

# =========================================================================
#  DESIGN 1 — NOIR & GOLD   (dark, centered classic)
# =========================================================================
def d1_front():
    b = [bg(INK), f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#glow)"/>']
    ow = 44
    ox = CX - ow / 2
    img, oh = image(OWL, ox, 22, ow, OWL_AR)
    b.append(img)
    b.append(f'<rect x="{CX-15}" y="{22+oh+6:.1f}" width="30" height="0.7" fill="{GOLD}"/>')
    b.append(txt(CX, 100, INFO["name"], size=15, fill=WHITE, family=FONT_D, weight=600, anchor="middle"))
    b.append(txt(CX, 111, INFO["role"], size=4.6, fill=GOLD, weight=600, ls=1.6, anchor="middle"))
    # contact row
    y = 132
    b.append(txt(CX, y, f'{INFO["phone"]}', size=6, fill=SILVER, weight=400, anchor="middle"))
    b.append(txt(CX, y+9, f'{INFO["email"]}', size=6, fill=SILVER, weight=400, anchor="middle"))
    b.append(f'<rect x="{CX-38}" y="{y+13.5:.1f}" width="76" height="0.4" fill="{GOLD}" fill-opacity="0.35"/>')
    return svg("\n".join(b))

def d1_back():
    b = [bg(INK), f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#glow)"/>']
    lw = 96
    img, lh = image(LOCK, CX-lw/2, 34, lw, LOCK_AR)
    b.append(img)
    b.append(txt(CX, 132, INFO["tag"], size=6.6, fill=SILVER, family=FONT_D, italic=True, anchor="middle"))
    b.append(txt(CX, 144, INFO["web"], size=5.2, fill=GOLD, weight=600, ls=2, anchor="middle"))
    return svg("\n".join(b))

# =========================================================================
#  DESIGN 2 — IVORY EDITORIAL   (light, left-aligned)
# =========================================================================
def d2_front():
    b = [bg(PAPER)]
    b.append(f'<rect x="0" y="0" width="6" height="{H}" fill="url(#goldbar)"/>')
    ow = 34
    img, oh = image(OWL, 22, 22, ow, OWL_AR)
    b.append(img)
    b.append(txt(22, 84, INFO["name"], size=17, fill=INK, family=FONT_D, weight=600))
    b.append(txt(22, 94, INFO["role"], size=4.7, fill=GOLD_D, weight=600, ls=1.4))
    b.append(f'<rect x="22" y="102" width="26" height="0.8" fill="{GOLD}"/>')
    y = 115
    for ic, val in (("phone", INFO["phone"]), ("mail", INFO["email"]),
                    ("globe", INFO["web"]), ("pin", INFO["loc"])):
        b.append(icon(ic, 22, y-5.5, 6.4, GOLD_D, sw=1.8))
        b.append(txt(32.5, y, val, size=6, fill=INK2, weight=400))
        y += 9.0
    b.append(txt(248, 150, INFO["brand"], size=5, fill=GRAY_L, weight=700, ls=2.4, anchor="end"))
    return svg("\n".join(b))

def d2_back():
    b = [bg(INK), f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#glow)"/>']
    ow = 40
    img, oh = image(OWL, CX-ow/2, 34, ow, OWL_AR)
    b.append(img)
    b.append(wordmark(CX, 34+oh+18, 17))
    b.append(txt(CX, 34+oh+28, INFO["sub"], size=4.6, fill=GOLD, weight=600, ls=3.2, anchor="middle"))
    b.append(txt(CX, 144, INFO["tag"], size=6.2, fill=SILVER, family=FONT_D, italic=True, anchor="middle"))
    return svg("\n".join(b))

# =========================================================================
#  DESIGN 3 — GOLD SIDEBAR   (split panel)
# =========================================================================
def d3_front():
    panel = 96
    b = [bg(PAPER)]
    b.append(f'<rect x="0" y="0" width="{panel}" height="{H}" fill="{INK}"/>')
    b.append(f'<rect x="0" y="0" width="{panel}" height="{H}" fill="url(#glow)"/>')
    b.append(f'<rect x="{panel}" y="0" width="1.4" height="{H}" fill="{GOLD}"/>')
    ow = 46
    img, oh = image(OWL, panel/2-ow/2, 40, ow, OWL_AR)
    b.append(img)
    b.append(wordmark(panel/2, 40+oh+16, 11, ls=1.6))
    b.append(txt(panel/2, 40+oh+24, INFO["sub"], size=3.3, fill=GOLD, weight=600, ls=2.2, anchor="middle"))
    # right column
    rx = panel + 18
    b.append(txt(rx, 58, INFO["name"], size=15, fill=INK, family=FONT_D, weight=600))
    b.append(txt(rx, 68, INFO["role"], size=4.5, fill=GOLD_D, weight=600, ls=1.2))
    b.append(f'<rect x="{rx}" y="76" width="24" height="0.8" fill="{GOLD}"/>')
    y = 92
    for ic, val in (("phone", INFO["phone"]), ("mail", INFO["email"]),
                    ("globe", INFO["web"]), ("pin", INFO["loc"])):
        b.append(icon(ic, rx, y-5.5, 6.2, GOLD_D, sw=1.8))
        b.append(txt(rx+10.5, y, val, size=5.8, fill=INK2, weight=400))
        y += 9.4
    return svg("\n".join(b))

def d3_back():
    b = [bg(CHAR), f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#glow)"/>']
    lw = 92
    img, lh = image(LOCK, CX-lw/2, 36, lw, LOCK_AR)
    b.append(img)
    b.append(txt(CX, 132, INFO["tag"], size=6.4, fill="#d8d8d8", family=FONT_D, italic=True, anchor="middle"))
    b.append(txt(CX, 144, INFO["web"], size=5, fill=GOLD, weight=600, ls=2, anchor="middle"))
    return svg("\n".join(b))

# =========================================================================
#  DESIGN 4 — PORTRAIT PERSONAL   (headshot)
# =========================================================================
def d4_front():
    b = [bg(DARK), f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#glow)"/>']
    d = 92
    fx, fy = 24, (H-d)/2
    img, _ = image(FACE, fx, fy, d, FACE_AR)
    b.append(img)
    b.append(f'<circle cx="{fx+d/2}" cy="{fy+d/2}" r="{d/2+2.4}" fill="none" stroke="{GOLD}" stroke-width="1.1"/>')
    rx = fx + d + 18
    ow = 22
    imo, oh = image(OWL, rx, 24, ow, OWL_AR)
    b.append(imo)
    b.append(txt(rx, 74, INFO["name"], size=15.5, fill=WHITE, family=FONT_D, weight=600))
    b.append(txt(rx, 84, INFO["role"], size=4.4, fill=GOLD, weight=600, ls=1.2))
    b.append(f'<rect x="{rx}" y="92" width="22" height="0.8" fill="{GOLD}"/>')
    y = 106
    for ic, val in (("phone", INFO["phone"]), ("mail", INFO["email"]), ("globe", INFO["web"])):
        b.append(icon(ic, rx, y-5.5, 6, GOLD, sw=1.8))
        b.append(txt(rx+10, y, val, size=5.8, fill=SILVER, weight=400))
        y += 9.2
    return svg("\n".join(b))

def d4_back():
    b = [bg(DARK), f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#glow)"/>']
    ow = 42
    img, oh = image(OWL, CX-ow/2, 32, ow, OWL_AR)
    b.append(img)
    b.append(wordmark(CX, 32+oh+18, 16))
    b.append(txt(CX, 32+oh+27, INFO["sub"], size=4.4, fill=GOLD, weight=600, ls=3, anchor="middle"))
    b.append(txt(CX, 144, INFO["tag"], size=6.2, fill=SILVER, family=FONT_D, italic=True, anchor="middle"))
    return svg("\n".join(b))

# =========================================================================
#  DESIGN 5 — MINIMAL MONO   (light, typographic)
# =========================================================================
def d5_front():
    b = [bg(WHITE)]
    # faint owl watermark, right
    ow = 78
    img, oh = image(OWL, W-ow-4, 42, ow, OWL_AR, opacity=0.06)
    b.append(img)
    b.append(txt(24, 66, INFO["name"], size=20, fill=INK, family=FONT_D, weight=500))
    b.append(f'<rect x="24" y="76" width="200" height="0.5" fill="{GOLD}"/>')
    b.append(txt(24, 88, INFO["role"], size=5, fill=GOLD_D, weight=600, ls=1.8))
    y = 116
    b.append(txt(24, y, INFO["phone"], size=6, fill=INK2))
    b.append(txt(24, y+9, INFO["email"], size=6, fill=INK2))
    b.append(txt(24, y+18, INFO["web"], size=6, fill=INK2))
    b.append(txt(246, 136, INFO["brand"], size=5, fill=GRAY_L, weight=700, ls=2.6, anchor="end"))
    b.append(txt(246, 144, INFO["loc"], size=4.4, fill=GRAY_L, weight=400, anchor="end"))
    return svg("\n".join(b))

def d5_back():
    b = [bg(PAPER)]
    ow = 46
    img, oh = image(OWL, CX-ow/2, 40, ow, OWL_AR)
    b.append(img)
    b.append(wordmark(CX, 40+oh+16, 15, fill="url(#silverD)"))
    b.append(txt(CX, 40+oh+25, INFO["sub"], size=4, fill=GOLD_D, weight=600, ls=3, anchor="middle"))
    b.append(txt(CX, 144, INFO["web"], size=5, fill=GOLD_D, weight=600, ls=2, anchor="middle"))
    return svg("\n".join(b))

# =========================================================================
#  DESIGN 6 — EMBLEM PREMIUM   (dark, gold frame)
# =========================================================================
def d6_front():
    b = [bg(DARK), f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#glow)"/>']
    # frame inside safe area
    b.append(f'<rect x="18" y="18" width="{W-36}" height="{H-36}" fill="none" '
             f'stroke="{GOLD}" stroke-width="0.7" stroke-opacity="0.55"/>')
    ow = 40
    img, oh = image(OWL, CX-ow/2, 26, ow, OWL_AR)
    b.append(img)
    b.append(txt(CX, 98, INFO["name"], size=14.5, fill=WHITE, family=FONT_D, weight=600, anchor="middle"))
    b.append(txt(CX, 108, INFO["role"], size=4.3, fill=GOLD, weight=600, ls=1.5, anchor="middle"))
    y = 126
    b.append(txt(CX, y, f'{INFO["phone"]}   \u00b7   {INFO["email"]}', size=5.6, fill=SILVER, anchor="middle"))
    b.append(txt(CX, y+8.5, f'{INFO["web"]}   \u00b7   {INFO["loc"]}', size=5.6, fill=SILVER, anchor="middle"))
    return svg("\n".join(b))

def d6_back():
    b = [bg(INK), f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#glow)"/>']
    b.append(f'<rect x="18" y="18" width="{W-36}" height="{H-36}" fill="none" '
             f'stroke="{GOLD}" stroke-width="0.7" stroke-opacity="0.4"/>')
    # KP monogram
    b.append(txt(CX, 78, "KP", size=34, fill="url(#gold)", family=FONT_D, weight=700, anchor="middle"))
    b.append(f'<rect x="{CX-20}" y="88" width="40" height="0.6" fill="{GOLD}" fill-opacity="0.6"/>')
    b.append(wordmark(CX, 108, 13))
    b.append(txt(CX, 118, INFO["sub"], size=3.8, fill=GOLD, weight=600, ls=2.6, anchor="middle"))
    b.append(txt(CX, 138, INFO["tag"], size=5.8, fill=SILVER, family=FONT_D, italic=True, anchor="middle"))
    return svg("\n".join(b))

DESIGNS = {
    "01-noir-gold":       (d1_front, d1_back),
    "02-ivory-editorial": (d2_front, d2_back),
    "03-gold-sidebar":    (d3_front, d3_back),
    "04-portrait":        (d4_front, d4_back),
    "05-minimal-mono":    (d5_front, d5_back),
    "06-emblem-premium":  (d6_front, d6_back),
}

if __name__ == "__main__":
    for slug, (front, back) in DESIGNS.items():
        (OUT / f"{slug}-front.svg").write_text(front())
        (OUT / f"{slug}-back.svg").write_text(back())
        print("wrote", slug, "front + back")
    print(f"\n{len(DESIGNS)} designs x 2 sides = {len(DESIGNS)*2} SVGs -> {OUT}")
