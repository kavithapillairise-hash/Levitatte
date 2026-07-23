# Levitatte — Visiting Cards

Six print-ready visiting-card designs for **Kavitha Pillai** — *Managing Director & Head of
Training, Levitatte Learning & Development*. Each design has a **front** and a **back**.

Open **[`index.html`](index.html)** in a browser to preview all designs with download links.

## Contact details on the cards
- **Name:** Kavitha Pillai
- **Title:** Managing Director & Head of Training
- **Phone:** +91 7411 099 183
- **Email:** kavitha.pillai@levitatte.com
- **Web:** www.levitatte.com
- **Location:** Bengaluru, Karnataka, India

## The six designs
| # | Name | Style |
|---|------|-------|
| 01 | Noir & Gold | Classic centered, deep black with a gold hairline |
| 02 | Ivory Editorial | Light, left-aligned, gold edge bar + contact icons |
| 03 | Gold Sidebar | Split panel — brand block beside the details |
| 04 | Portrait | Personal card with the founder headshot in a gold ring |
| 05 | Minimal Mono | Typographic & airy, light with a faint owl watermark |
| 06 | Emblem Premium | Gold-framed with a **KP** monogram on the reverse |

## Print specification (give this to the printer)
| Property | Value |
|----------|-------|
| **Trim size** | 3.5 in × 2.0 in (88.9 mm × 50.8 mm) — standard business card |
| **Bleed** | 0.125 in (3.175 mm) on every side — artwork extends to the canvas edge |
| **Canvas (with bleed)** | 3.75 in × 2.25 in (95.25 mm × 57.15 mm) |
| **Safe area** | 0.125 in (3 mm) inside the trim — all text/logos are kept inside |
| **Vector files** | `print/*.pdf` and `svg/*.svg` — resolution-independent |
| **Raster proofs** | `preview/*.png` at **300 DPI** (1125 × 675 px) |
| **Recommended stock** | 350–400 gsm matte or soft-touch; gold designs look best with **spot-gold foil** on `#c9a84c` areas (optional) |

> **Colour note:** files are authored in **RGB** (gold `#c9a84c`, black `#111111`). Most digital
> presses accept RGB and convert to CMYK automatically. If your printer requires CMYK, ask them to
> convert, or request a CMYK proof before the full run.

## Folder layout
```
business-cards/
├── index.html          # visual gallery / viewer (open this)
├── generate_cards.py   # regenerates the SVGs from brand assets
├── assets/             # owl-mark, full lockup, circular headshot (embedded into the SVGs)
├── svg/                # 12 master vector files (6 designs × front/back)
├── print/             # 12 print-ready vector PDFs (3.75×2.25 in incl. bleed)
└── preview/            # 12 × 300 DPI PNG proofs + _contact-sheet.png
```

## Regenerating
Requires `rsvg-convert` (librsvg) and the *Inter* + *Playfair Display* fonts.
```bash
python3 generate_cards.py                       # writes svg/
for f in svg/*.svg; do b=$(basename "$f" .svg);
  rsvg-convert -f pdf -o "print/$b.pdf" "$f";
  rsvg-convert -f png --dpi-x 300 --dpi-y 300 -o "preview/$b.png" "$f";
done
```
