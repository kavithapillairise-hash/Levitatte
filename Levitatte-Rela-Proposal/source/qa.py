"""
Automated QA gate for the Levitatte -> Rela proposal.
Checks the assembled copy.json AND the extracted PDF text.
Exit 0 = clean, 1 = failures.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

REQUIRED_SECTIONS = [
    "cover-letter", "context", "objectives", "scope-of-work", "induction",
    "sequencing-logic", "curriculum", "calendar", "methodology",
    "role-tracks", "takeaways", "leadership", "ttt",
    "approach", "deliverables", "measurement", "commercials",
    "assumptions", "outcomes", "closing",
]

# phrases that would imply the deal is already agreed
FORBIDDEN = [
    r"as (?:we )?(?:verbally )?(?:agreed|discussed|confirmed)",
    r"as per our (?:discussion|conversation|agreement)",
    r"further to our (?:discussion|conversation|meeting)",
    r"further to the discussion",
    r"pursuant to our (?:discussion|agreement)",
    r"following our (?:discussion|conversation)",
    r"already (?:agreed|confirmed|finalis?zed|finalised)",
    r"verbally (?:agreed|confirmed|discussed)",
    r"has been (?:agreed|confirmed) ",
    r"our recent (?:discussion|conversation|meeting)",
    r"thank you for (?:confirming|the confirmation)",
]

HYPE = [
    "world-class", "cutting-edge", "game-changing", "revolutionary", "synergy",
    "synergies", "leverage", "supercharge", "unlock the", "best-in-class",
    "paradigm", "seamlessly", "turnkey", "holistic solution", "one-stop",
]

# substantive defects the adversarial critics found; these must never regress
REGRESSIONS = [
    "retain more than two directions",
    "single most reliable predictor",
    "single most common reason",
    "least expensive and least resisted",
    "largest allocation in the first half",
    "M1 to M9 form the common foundation",
    "matter of individual disposition",
    "twenty-five years of work in behavioural",
    "billing, nursing support, housekeeping and security each work",
    "issued in the first fortnight rather than at the end",
]

DISCLAIMER = (
    "Clinical, statutory and policy-specific training content will be developed or "
    "delivered in coordination with authorised hospital representatives and "
    "subject-matter experts."
)

# numbers that must appear somewhere, and numbers that must NOT
_FEE = os.environ.get("FEE", "150000")
_SCALE = {
    "150000": ["1,50,000", "4,50,000", "1,35,000", "4,05,000", "15,000", "45,000"],
    "200000": ["2,00,000", "6,00,000", "1,80,000", "5,40,000", "20,000", "60,000"],
}
assert _FEE in _SCALE, f"unknown FEE scale {_FEE}"
MUST_APPEAR = _SCALE[_FEE] + ["39", "156", "30", "90", "194J", "Form 16A"]
# figures from the OTHER scale must not leak into this variant
STALE = [x for k, v in _SCALE.items() if k != _FEE for x in v if x not in _SCALE[_FEE]]
BAD_NUMBER_FORMAT = [r"\b150,000\b", r"\b450,000\b", r"\bRs\.?\s?1,?50000\b", r"\b1170\b(?!,)"]

fails, warns = [], []


def flat_text(data):
    out = []
    for s in data["sections"]:
        out.append(s.get("eyebrow", ""))
        out.append(s.get("title", ""))
        out.append(s.get("intro", "") or "")
        for b in s.get("blocks", []):
            out.append(b.get("text", "") or "")
            for it in b.get("items", []) or []:
                out.append(it)
            for c in b.get("columns", []) or []:
                out.append(c)
            for r in b.get("rows", []) or []:
                out.extend(str(x) for x in r)
    return "\n".join(out)


def main():
    copy_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "copy.json")
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "proposal.pdf")
    data = json.load(open(copy_path))
    text = flat_text(data)
    low = text.lower()

    # 1. section completeness + order
    ids = [s["id"] for s in data["sections"]]
    missing = [x for x in REQUIRED_SECTIONS if x not in ids]
    if missing:
        fails.append(f"missing sections: {missing}")
    if ids[: len(REQUIRED_SECTIONS)] != REQUIRED_SECTIONS:
        warns.append(f"section order differs from canonical:\n   got {ids}")

    # 2. forbidden prior-agreement language
    for pat in FORBIDDEN:
        for m in re.finditer(pat, low):
            ctx = text[max(0, m.start() - 70): m.end() + 70].replace("\n", " ")
            fails.append(f"prior-agreement language /{pat}/ -> ...{ctx}...")

    # 3. hype
    for h in HYPE:
        if h in low:
            warns.append(f"hype word present: '{h}'")

    # 3b. regression guard on the adversarially-found defects
    for r in REGRESSIONS:
        if r.lower() in low:
            fails.append(f"REGRESSION of a fixed defect: '{r}'")

    # 4. exclamation marks / em-dash connectors
    if "!" in text:
        fails.append("exclamation mark present")
    n_em = text.count("—")
    if n_em:
        warns.append(f"{n_em} em-dash(es) present (brief prefers full stops/commas)")

    # 5. disclaimer verbatim
    norm = re.sub(r"\s+", " ", text)
    if re.sub(r"\s+", " ", DISCLAIMER) not in norm:
        fails.append("mandatory clinical/statutory disclaimer missing or altered")

    # 6. numbers present + Indian formatting
    for n in MUST_APPEAR:
        if n not in text:
            fails.append(f"required figure absent from copy: {n}")
    for pat in BAD_NUMBER_FORMAT:
        if re.search(pat, text):
            fails.append(f"non-Indian number formatting matched /{pat}/")
    for st in STALE:
        if st in text:
            fails.append(f"figure from the other fee scale leaked in: {st}")

    # 7. module table sums to 39 and calendar has 13 weeks
    mod_tables, cal_tables = [], []
    for s in data["sections"]:
        for b in s.get("blocks", []):
            if b.get("type") != "table":
                continue
            cols = [c.lower() for c in (b.get("columns") or [])]
            if "sessions" in cols:
                mod_tables.append(b)
            if cols and cols[0].startswith("week"):
                cal_tables.append(b)

    if not mod_tables:
        fails.append("no module table with a Sessions column found")
    for t in mod_tables:
        idx = [c.lower() for c in t["columns"]].index("sessions")
        total_row, body_sum = None, 0
        for r in t["rows"]:
            label = str(r[0]).strip().lower()
            try:
                v = int(re.sub(r"[^0-9]", "", str(r[idx])) or 0)
            except Exception:
                continue
            if label in ("total", "totals"):
                total_row = v
            else:
                body_sum += v
        if body_sum != 39:
            fails.append(f"module sessions sum to {body_sum}, expected 39")
        if total_row is not None and total_row != 39:
            fails.append(f"module table total row says {total_row}, expected 39")

    if not cal_tables:
        fails.append("no 13-week calendar table found")
    for t in cal_tables:
        if len(t["rows"]) != 13:
            fails.append(f"calendar has {len(t['rows'])} rows, expected 13")

    # 8. all 8 role groups present in the takeaways section
    groups = ["front-office", "patient relations", "billing", "nursing",
              "housekeeping", "security", "supervisor", "manager"]
    tk = next((s for s in data["sections"] if s["id"] == "takeaways"), None)
    if tk:
        tkl = flat_text({"sections": [tk]}).lower()
        for g in groups:
            if g not in tkl:
                fails.append(f"role group '{g}' missing from takeaways section")

    # 9. PDF-level checks
    if os.path.exists(pdf_path):
        ptext = subprocess.run(["pdftotext", pdf_path, "-"], capture_output=True,
                               text=True).stdout
        pages = subprocess.run(["pdfinfo", pdf_path], capture_output=True, text=True).stdout
        npages = int(re.search(r"Pages:\s+(\d+)", pages).group(1))
        print(f"   pdf pages: {npages}")
        if npages < 14:
            warns.append(f"only {npages} pages; expected a substantial document")
        if "REPLACE" in ptext or "TBD" in ptext or "Lorem" in ptext:
            fails.append("placeholder text found in PDF")
        if "kavithapillairise@gmail.com" in ptext:
            fails.append("stale gmail address present; must be kavitha.pillai@levitatte.com")
        for n in _SCALE[_FEE][:2]:          # fee and engagement total, for the active scale
            if n not in ptext:
                fails.append(f"figure {n} did not survive into the PDF")
    else:
        warns.append(f"pdf not found at {pdf_path}, skipped PDF checks")

    # report
    print(f"\n   sections: {len(data['sections'])}")
    print(f"   words   : {len(text.split()):,}")
    print(f"\n{'='*64}")
    for w in warns:
        print(f"WARN  {w}")
    for f in fails:
        print(f"FAIL  {f}")
    print(f"{'='*64}")
    print(f"{len(fails)} failures, {len(warns)} warnings")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
