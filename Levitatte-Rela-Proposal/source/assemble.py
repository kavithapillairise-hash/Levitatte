"""Assemble copy.json from either final.json (synthesised) or drafts.json (4 slices)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

ORDER = [
    "cover-letter", "context", "objectives", "scope-of-work", "induction",
    "sequencing-logic", "curriculum", "calendar", "methodology",
    "role-tracks", "takeaways", "leadership", "ttt",
    "approach", "deliverables", "measurement", "commercials",
    "assumptions", "outcomes", "closing",
]


def load_sections(src):
    p = os.path.join(HERE, src)
    data = json.load(open(p))
    if isinstance(data, dict) and "sections" in data:
        return data["sections"]
    # drafts.json = list of {sections:[...]}
    out = []
    for d in data:
        out.extend(d.get("sections", []))
    return out


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "drafts.json"
    secs = load_sections(src)
    by_id = {}
    for s in secs:
        by_id.setdefault(s["id"], s)

    ordered, missing = [], []
    for sid in ORDER:
        if sid in by_id:
            ordered.append(by_id[sid])
        else:
            missing.append(sid)
    extra = [s["id"] for s in secs if s["id"] not in ORDER]

    meta = json.load(open(os.path.join(HERE, "meta.json")))
    json.dump({"meta": meta, "sections": ordered},
              open(os.path.join(HERE, "copy.json"), "w"), indent=1)

    print(f"source        : {src}")
    print(f"sections found: {len(secs)}  ->  ordered {len(ordered)}")
    if missing:
        print(f"MISSING       : {missing}")
    if extra:
        print(f"EXTRA (dropped): {extra}")
    print("wrote copy.json")


if __name__ == "__main__":
    main()
