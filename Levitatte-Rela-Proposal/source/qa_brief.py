"""QA gate for the concise (4-page) edition. Reuses the full document's rule sets."""
import json
import os
import re
import subprocess
import sys

import qa as Q

HERE = os.path.dirname(os.path.abspath(__file__))

REQUIRED = ["proposition", "glance", "sequence", "takeaways", "delivery", "close"]
GROUPS = ["front office", "patient relations", "billing", "nursing",
          "housekeeping", "security", "supervisor", "manager"]
# every figure that must survive the condensation
_UNITS = {
    "150000": ["2,900", "96", "3,125", "104"],
    "200000": ["3,850", "128", "4,167", "139"],
}
FIGURES = Q.MUST_APPEAR + ["4,680"] + _UNITS[os.environ.get("FEE", "150000")]

fails, warns = [], []


def main():
    src = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "brief_copy.json")
    data = json.load(open(src))
    pdf = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "proposal_brief.pdf")
    text = Q.flat_text(data)
    low = text.lower()

    ids = [s["id"] for s in data["sections"]]
    for r in REQUIRED:
        if r not in ids:
            fails.append(f"missing section: {r}")

    for pat in Q.FORBIDDEN:
        for m in re.finditer(pat, low):
            fails.append(f"prior-agreement language /{pat}/ -> ...{text[max(0,m.start()-60):m.end()+60]}...")
    for r in Q.REGRESSIONS:
        if r.lower() in low:
            fails.append(f"regression of a fixed defect: '{r}'")
    for h in Q.HYPE:
        if h in low:
            warns.append(f"hype word: '{h}'")
    if "!" in text:
        fails.append("exclamation mark present")

    norm = re.sub(r"\s+", " ", text)
    if re.sub(r"\s+", " ", Q.DISCLAIMER) not in norm:
        fails.append("mandatory clinical/statutory disclaimer missing or altered")

    for f in FIGURES:
        if f not in text:
            fails.append(f"figure lost in condensation: {f}")
    for pat in Q.BAD_NUMBER_FORMAT:
        if re.search(pat, text):
            fails.append(f"non-Indian number formatting /{pat}/")

    # module table must still sum to 39 across 12 modules
    for s in data["sections"]:
        for b in s.get("blocks", []):
            if b.get("type") != "table":
                continue
            cols = [c.lower() for c in b.get("columns", [])]
            if "sessions" not in cols:
                continue
            i = cols.index("sessions")
            body, total, nmod = 0, None, 0
            for row in b["rows"]:
                try:
                    v = int(re.sub(r"[^0-9]", "", str(row[i])) or 0)
                except Exception:
                    continue
                if str(row[0]).strip().lower() == "total":
                    total = v
                else:
                    body += v
                    nmod += 1
            if nmod != 12:
                fails.append(f"module table has {nmod} modules, expected 12")
            if body != 39:
                fails.append(f"module sessions sum to {body}, expected 39")
            if total != 39:
                fails.append(f"module total row says {total}, expected 39")

    tk = next((s for s in data["sections"] if s["id"] == "takeaways"), None)
    if tk:
        t = Q.flat_text({"sections": [tk]}).lower()
        for g in GROUPS:
            if g not in t:
                fails.append(f"role group '{g}' missing from takeaways")

    if os.path.exists(pdf):
        info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
        n = int(re.search(r"Pages:\s+(\d+)", info).group(1))
        print(f"   pdf pages: {n}")
        if n > 4:
            fails.append(f"{n} pages; the concise edition must be 3 to 4")
        if n < 3:
            warns.append(f"only {n} pages")
        ptext = subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True).stdout
        if "kavithapillairise@gmail.com" in ptext:
            fails.append("stale gmail address present")
        for f in Q.MUST_APPEAR[:2]:        # fee and engagement total, for the active scale
            if f not in ptext:
                fails.append(f"{f} did not survive into the PDF")

    print(f"\n   sections: {len(data['sections'])}")
    print(f"   words   : {len(text.split()):,}")
    print("=" * 64)
    for w in warns:
        print(f"WARN  {w}")
    for f in fails:
        print(f"FAIL  {f}")
    print("=" * 64)
    print(f"{len(fails)} failures, {len(warns)} warnings")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
