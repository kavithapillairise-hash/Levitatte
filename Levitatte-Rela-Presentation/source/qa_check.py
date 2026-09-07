"""
QA gate for the Levitatte -> Rela presentation and its two-page companion.

Reads the built PDFs (not the source), because what matters is what the hospital will actually
see. Exit 0 = clean, 1 = failures.

    python3 qa_check.py ../Levitatte-Rela-5-Slide-Presentation.pdf ../Levitatte-Rela-2-Page-Proposal.pdf
"""
import re
import subprocess
import sys

import content as C

# ── the owner's standing instruction for this edition ───────────────────────────
# "after 200000 just mention the words taxes as applicable .. do not do deductions or any such
# calculations" and "Just GST as applicable.. do not mention the word additional".
FORBIDDEN = [
    (r"tax deducted at source", "tax-deducted-at-source wording"),
    (r"\bTDS\b", "TDS"),
    (r"194\s?J", "section 194J"),
    (r"Form\s?16A", "Form 16A"),
    (r"\bPAN\b", "PAN"),
    (r"\bTAN\b", "TAN"),
    (r"less tax", "a deduction line"),
    (r"payable to levitatte", "a net-payable line"),
    (r"1,80,000", "net-of-deduction monthly figure"),
    (r"5,40,000", "net-of-deduction engagement figure"),
    (r"\b20,000\b", "monthly deduction figure"),
    (r"\b60,000\b", "engagement deduction figure"),
    (r"3,850", "per-hour arithmetic"),
    (r"4,167", "per-hour arithmetic"),
    (r"4,680", "participant-hour arithmetic"),
    (r"per participant-training-hour", "per-participant-hour arithmetic"),
    (r"\badditional\b", 'the word "additional"'),
    (r"\bgross\b", "gross-versus-net framing"),
    (r"\bexcluding GST\b", "excluding-GST framing"),
    (r"\bplus GST\b", "plus-GST framing"),
]

REQUIRED = [
    ("2,00,000", "the monthly fee"),
    ("6,00,000", "the engagement value"),
    ("GST as applicable", "the GST wording"),
    ("39", "session count"),
    ("156", "facilitator-led hours"),
    ("30", "batch size"),
    ("90", "engagement length"),
    ("Kavitha Pillai", "the contact name"),
    ("+91 7411 099 183", "the contact number"),
]

# house style, carried over from the proposal's own gate
HYPE = ["world-class", "cutting-edge", "game-changing", "revolutionary", "synergy", "synergies",
        "leverage", "supercharge", "best-in-class", "paradigm", "seamlessly", "turnkey",
        "one-stop", "holistic solution"]

PRIOR_AGREEMENT = [
    r"as (?:we )?(?:verbally )?(?:agreed|discussed|confirmed)",
    r"as per our (?:discussion|conversation|agreement)",
    r"further to our (?:discussion|conversation|meeting)",
    r"following our (?:discussion|conversation)",
    r"already (?:agreed|confirmed|finalis[sz]ed)",
]

BAD_NUMBERS = [r"\b200,000\b", r"\b600,000\b", r"\b150,000\b", r"\bRs\.?\s?200000\b"]

# checked against the whitespace-free projection, so tracked headings cannot smuggle these past
SQUASH_FORBIDDEN = [r"1,80,000", r"5,40,000", r"taxdeductedatsource", r"194j", r"form16a",
                    r"lesstax", r"payabletolevitatte", r"3,850", r"4,167", r"4,680"]

# every capability word the owner asked to see reflected in the material
VOCABULARY = [
    "self-efficacy", "awareness", "quality", "who we are", "brand awareness",
    "industry-specific knowledge", "empathy enhancement", "conflict resolution",
    "personality", "image", "self-motivation", "stress management",
    "interdepartmental", "proactive service", "service excellence", "service recovery",
    "crisis management", "emotional intelligence", "forecasted", "case studies",
    "incident report", "narrative of real experience", "assessment before and after",
    "emergency situational awareness", "protocol",
]

ROLE_GROUPS = ["front office", "patient relations", "billing", "nursing",
               "housekeeping", "security", "supervisor", "manager"]


def text_of(pdf):
    # NOT -layout: that mode preserves visual columns, so a wrapped sentence in column 3 is
    # interleaved with columns 1 and 2 and no phrase survives intact.
    return subprocess.run(["pdftotext", pdf, "-"],
                          capture_output=True, text=True, check=True).stdout


def squash(s):
    """Drop all whitespace.

    Letter-spaced headings extract from the PDF as "B R A N D  AWA R E N E S S", so phrase
    presence has to be tested against a whitespace-free projection of both sides.
    """
    return re.sub(r"\s+", "", s).lower()


def pages_of(pdf):
    out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True, check=True).stdout
    return int(re.search(r"Pages:\s+(\d+)", out).group(1))


def check(pdf, want_pages, label, fails, warns):
    n = pages_of(pdf)
    if n != want_pages:
        fails.append(f"{label}: {n} pages, expected {want_pages}")
    raw = text_of(pdf)
    flat = re.sub(r"\s+", " ", raw)
    low = flat.lower()

    sq = squash(flat)
    for pat, why in FORBIDDEN:
        m = re.search(pat, flat, re.I)
        if m:
            ctx = flat[max(0, m.start() - 60):m.end() + 60]
            fails.append(f"{label}: {why} present -> ...{ctx}...")
    for pat in SQUASH_FORBIDDEN:
        if re.search(pat, sq, re.I):
            fails.append(f"{label}: /{pat}/ present in letter-spaced text")

    for token, why in REQUIRED:
        if squash(token) not in sq:
            fails.append(f"{label}: {why} ({token}) missing")

    norm_disc = re.sub(r"\s+", " ", C.DISCLAIMER)
    if squash(norm_disc) not in sq:
        fails.append(f"{label}: mandatory clinical/statutory disclaimer missing or altered")

    if "!" in flat:
        fails.append(f"{label}: exclamation mark present")
    if "—" in flat:
        warns.append(f"{label}: em-dash present (house style is en dashes)")
    for h in HYPE:
        if h in low:
            warns.append(f"{label}: hype word '{h}'")
    for pat in PRIOR_AGREEMENT:
        if re.search(pat, low):
            fails.append(f"{label}: language implying the deal is already agreed (/{pat}/)")
    for pat in BAD_NUMBERS:
        if re.search(pat, flat):
            fails.append(f"{label}: non-Indian digit grouping (/{pat}/)")

    for g in ROLE_GROUPS:
        if squash(g) not in sq:
            fails.append(f"{label}: role group '{g}' missing")

    # the twelve modules and their 39 sessions must survive every condensation
    for i in range(1, 13):
        if not re.search(rf"m{i}[a-z]", sq):
            fails.append(f"{label}: module M{i} missing")
    if "39" not in flat:
        fails.append(f"{label}: session total 39 missing")

    return sq


def main():
    deck = sys.argv[1]
    two = sys.argv[2]
    fails, warns = [], []

    sq_deck = check(deck, 5, "deck", fails, warns)
    sq_two = check(two, 2, "2-pager", fails, warns)
    both = sq_deck + "\n" + sq_two

    missing_vocab = [v for v in VOCABULARY if squash(v) not in both]
    if missing_vocab:
        fails.append("requested vocabulary absent from BOTH artefacts: "
                     + ", ".join(missing_vocab))
    only_one = [v for v in VOCABULARY
                if (squash(v) in sq_deck) != (squash(v) in sq_two)]
    if only_one:
        warns.append("vocabulary present in only one artefact (acceptable, the 2-pager is the "
                     "condensed edition): " + ", ".join(only_one))

    # the content module's own invariants
    assert sum(m[3] for m in C.MODULES) == 39

    print("=" * 74)
    for w in warns:
        print(f"WARN  {w}")
    for f in fails:
        print(f"FAIL  {f}")
    print("=" * 74)
    print(f"{len(fails)} failures, {len(warns)} warnings")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
