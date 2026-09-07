# Levitatte → Dr. Rela Institute & Medical Centre

Two deliverables for the 90-day learning and development engagement at **Rs 2,00,000 per month,
GST as applicable**, both generated from one shared copy module so a figure or a term cannot
drift between them.

| File | What it is |
|---|---|
| `Levitatte-Rela-5-Slide-Presentation.pptx` | The deck, editable in PowerPoint or Keynote (16:9, 233 live text frames, no flattened images) |
| `Levitatte-Rela-5-Slide-Presentation.pdf` | The same deck, for sending |
| `Levitatte-Rela-2-Page-Proposal.docx` | The less detailed 2-page companion, editable in Word |
| `Levitatte-Rela-2-Page-Proposal.pdf` | The same companion, for sending |

## The five slides

1. **Cover** — brand lockup, the engagement in figures (90 / 39 / 156 / 12 / 30) and the fee.
2. **Every interaction is part of care** — the proposition, the nine capabilities the programme
   builds, and who we are.
3. **The twelve modules** — the full curriculum table (12 modules, 39 sessions), why the order is
   what it is, and how the cohorts run.
4. **How it runs** — how we teach, the five stages, deliverables, the four levels of reporting,
   and what each of the eight role groups keeps.
5. **Commercial terms** — the fee, the engagement at a glance, what the fee covers, terms, and
   what we would need from the hospital.

## Commercials wording

The fee is stated as **Rs 2,00,000 per month, fixed. GST as applicable.** and
**Rs 6,00,000 for the 90-day engagement**. There is deliberately no tax-deducted-at-source
table, no net-payable figures, no section 194J or Form 16A wording, no per-hour or
per-participant-hour arithmetic, and the word "additional" is not used anywhere. `qa_check.py`
fails the build if any of that reappears.

Everything else — the module table, the cohort plan, the role outcomes, the five stages, the
deliverables, the four-level reporting with its honesty caveat, what the hospital provides, the
invoicing and calendar terms, and the mandatory clinical/statutory note — is carried across from
`Levitatte-Rela-Hospital-LD-Proposal-4-page-200000-Post-TDS.pdf`.

## Rebuilding

```bash
bash source/build.sh
```

Regenerates both files, asserts the deck is 5 slides and the companion is exactly 2 pages, then
runs the QA gate. Needs `python-pptx`, `python-docx`, LibreOffice (`soffice`) and poppler
(`pdfinfo`/`pdftotext`), plus Inter and Playfair Display installed locally.

## source/

| File | Role |
|---|---|
| `content.py` | All copy and figures. Single source of truth; asserts its own invariants on import (12 modules, 39 sessions, 8 role groups). |
| `deck.py` | Builds the 5-slide PPTX. Layout is derived, not eyeballed: block heights come from `measure.py`, `distribute()`/`fit_blocks()` place them, and `guard()` refuses to save a file with an off-slide, non-positive or footer-crossing shape. |
| `twopager.py` | Builds the 2-page DOCX. `BODY_PT`/`LINE` tune the whole document in one place. |
| `measure.py` | Exact text measurement against the real font files, including letter-spacing and mixed-format lines. |
| `qa_check.py` | Reads the built PDFs and checks fee wording, absent deduction arithmetic, the verbatim disclaimer, house style, Indian digit grouping, all 12 modules, all 8 role groups, and the requested vocabulary. |
| `docx_brand.py` | The proposal's own renderer, copied verbatim so the companion is byte-for-byte on-brand. |
| `owl_refined.png` | The refined owl, as used in the proposal. |

Palette and typefaces are lifted from the existing proposal: ivory `#FAF8F3`, ink `#201C15`,
antique gold `#937425` / `#B08930`, Playfair Display for display, Inter for text.

### Notes for whoever edits this next

- Leading is quoted **absolutely** (a multiple of the point size) and converted to the renderer's
  percentage-of-natural-line-height at write time. Inter's natural line height is 1.22 and
  Playfair's 1.35, so treating a spacing multiple as if it applied to the point size undersizes
  every block by that much.
- `pdftotext -layout` interleaves the deck's columns and destroys phrase continuity; the gate uses
  plain extraction, and compares against a whitespace-free projection because letter-spaced
  headings extract as `B R A N D  AWA R E N E S S`.
- python-pptx attaches a `<p:style>` element referencing the theme's effects; LibreOffice honours
  it and draws a drop shadow on every card. `rect()` strips it.
