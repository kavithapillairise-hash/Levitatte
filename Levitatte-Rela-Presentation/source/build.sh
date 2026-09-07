#!/usr/bin/env bash
# Rebuild both artefacts from source and refuse to finish if either is wrong.
#
#   bash source/build.sh          # run from the project root
#
# Asserts: the deck is 5 slides, the companion is exactly 2 pages of A4, and qa_check.py
# passes (fee wording, no deduction arithmetic, disclaimer verbatim, house style).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$HERE")"
cd "$ROOT"

DECK="Levitatte-Rela-5-Slide-Presentation"
TWO="Levitatte-Rela-2-Page-Proposal"

echo "── deck ─────────────────────────────────────────────────────────"
python3 "$HERE/deck.py" "$DECK.pptx"
rm -f "$DECK.pdf"
soffice --headless --convert-to pdf --outdir . "$DECK.pptx" >/dev/null 2>&1
n=$(pdfinfo "$DECK.pdf" | awk '/^Pages/{print $2}')
[ "$n" = "5" ] || { echo "FAIL: deck is $n slides, expected 5"; exit 1; }
echo "   $DECK.pdf : $n slides"

echo "── two-page companion ───────────────────────────────────────────"
python3 "$HERE/twopager.py" "$TWO.docx"
rm -f "$TWO.pdf"
soffice --headless --convert-to pdf --outdir . "$TWO.docx" >/dev/null 2>&1
n=$(pdfinfo "$TWO.pdf" | awk '/^Pages/{print $2}')
[ "$n" = "2" ] || { echo "FAIL: companion is $n pages, expected 2 (tune BODY_PT / LINE)"; exit 1; }
echo "   $TWO.pdf : $n pages"

echo "── qa gate ──────────────────────────────────────────────────────"
python3 "$HERE/qa_check.py" "$DECK.pdf" "$TWO.pdf"

# LibreOffice leaves lock files behind if it was interrupted
rm -f .~lock.*# 2>/dev/null || true
echo "done."
