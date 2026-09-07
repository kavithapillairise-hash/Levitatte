"""
Canonical copy for the Levitatte -> Rela 5-slide presentation and its 2-page companion.

One source of truth: deck.py and twopager.py both read from here, so a figure or a term can
never drift between the two artefacts. Terms and conditions are carried across from
Levitatte-Rela-Hospital-LD-Proposal-4-page-200000-Post-TDS.pdf.

DELIBERATE DIVERGENCE FROM THAT SOURCE (owner's instruction, this edition): the fee reads
"Rs 2,00,000 per month, fixed. GST as applicable." and nothing else. No tax-deducted-at-source
table, no net-payable figures, no section 194J or Form 16A wording, no per-hour or
per-participant-hour arithmetic, and the word "additional" is not used. qa_check.py fails the
build if any of that reappears.

House rules (also enforced by qa_check.py): no exclamation marks, no hype vocabulary, no
prior-agreement language, en dashes only, Indian digit grouping, disclaimer verbatim.
"""

# ── masthead / identity ─────────────────────────────────────────────────────────
META = {
    "brand": "LEVITATTE",
    "brand_sub": "LEARNING  &  DEVELOPMENT",
    "descriptor": "END-TO-END LEARNING & DEVELOPMENT SOLUTIONS FOR HEALTHCARE ORGANISATIONS",
    "title_lines": ["Transforming Hospital Teams.", "Elevating Every Patient Experience."],
    "deck_title_lines": ["Elevating Healthcare", "Through People."],
    "subtitle": "A structured 90-day learning and development programme",
    "prepared_for": "Prepared for the leadership of Dr. Rela Institute & Medical Centre, Chromepet, Chennai",
    "client_short": "DR. RELA INSTITUTE & MEDICAL CENTRE",
    "date": "AUGUST 2026",
    "tagline": "Competent.  Compassionate.  Confident.  Accountable.  Patient-First.",
    "footer": "LEVITATTE LEARNING & DEVELOPMENT     ·     PROPOSAL FOR DR. RELA INSTITUTE & MEDICAL CENTRE",
    "contact_name": "Kavitha Pillai",
    "contact_role": "Managing Director & Head of Training",
    "contact_line": "+91 7411 099 183     ·     KAVITHA.PILLAI@LEVITATTE.COM     ·     WWW.LEVITATTE.COM",
    "confidential": "Private and confidential. Prepared exclusively for the leadership of Dr. Rela Institute & Medical Centre.",
}

# mandatory, verbatim, never reworded
DISCLAIMER = (
    "Clinical, statutory and policy-specific training content will be developed or "
    "delivered in coordination with authorised hospital representatives and "
    "subject-matter experts."
)

# ── 01 the proposition ──────────────────────────────────────────────────────────
PROPOSITION = [
    "Every patient interaction shapes the reputation of a hospital. From the first telephone "
    "call and the registration counter through treatment coordination, billing and discharge, "
    "patients and their families expect clarity, compassion, professionalism and confidence.",
    "Across a full episode of care the treating consultant is present for only some of the "
    "patient's time in the building. The rest belongs to front office, patient relations, "
    "billing, nursing and clinical support, housekeeping and security, who hold the experience "
    "together at moments the clinician never sees. Clinical excellence can be concentrated in "
    "specialists; the experience of being cared for cannot, because it is assembled touchpoint "
    "by touchpoint. That consistency is a capability, and it is trainable.",
]

PULLQUOTE = (
    "Quality is not what the hospital intends. It is what the patient remembers about the way "
    "they were treated at every touchpoint."
)

# the nine capabilities the programme builds
PILLARS = [
    ("AWARENESS & SELF-EFFICACY",
     "Self-awareness of the standard one is setting, and the confidence to hold it without being supervised into it."),
    ("PERSONALITY & IMAGE",
     "Professional presence, bearing and grooming: the image the hospital projects before a word is spoken."),
    ("EMOTIONAL INTELLIGENCE",
     "Empathy enhancement sessions, self-regulation under pressure, and the protection of patient dignity and privacy."),
    ("SERVICE EXCELLENCE",
     "Proactive service, quality at every touchpoint, and the honest management of expectations and delays."),
    ("SERVICE RECOVERY & CRISIS MANAGEMENT",
     "Complaint handling, conflict resolution, de-escalation, incident reporting and closing the loop with families."),
    ("COORDINATION & COMMUNICATION",
     "Interdepartmental connection, effective handovers and escalation protocol that holds across shifts."),
    ("RESILIENCE & SELF-MOTIVATION",
     "Stress management, compassion fatigue, accountability and the discipline to sustain a standard on a hard day."),
    ("BRAND AWARENESS",
     "Every employee carries the hospital's brand. Each interaction either builds it or quietly spends it."),
    ("FORECASTED THINKING",
     "Reading the day ahead: anticipating load, delay and risk in daily operations instead of reacting to them."),
]

WHO_WE_ARE = (
    "Levitatte brings a founder with more than twenty-five years in behavioural, communication "
    "and service capability building, grounded in NLP and organisational behavioural psychology, "
    "with prior healthcare engagements at Fortis and Cloud9 Hospitals. Industry-specific "
    "knowledge of hospital floors shapes every module: the content is customised against your own "
    "policies, SOPs and service standards rather than delivered from a generic library."
)

# ── 02 commercial terms ─────────────────────────────────────────────────────────
GLANCE = [
    ("ENGAGEMENT DURATION", "90 days (approximately 13 weeks)"),
    ("TRAINING DAYS", "Every Wednesday, Thursday and Friday"),
    ("SESSION DURATION", "4 hours per session"),
    ("BATCH SIZE", "Up to 30 participants per batch"),
    ("SESSIONS IN THE ENGAGEMENT", "Up to 39 (36 to 39 subject to start date and hospital holidays)"),
    ("FACILITATOR-LED HOURS", "Up to 156 hours (144 to 156)"),
    ("PROFESSIONAL FEE", "Rs 2,00,000 per month, fixed"),
    ("GST", "As applicable"),
    ("TOTAL ENGAGEMENT VALUE", "Rs 6,00,000 for the 90-day engagement"),
]

FEE_HEADLINE = "Rs 2,00,000"
FEE_HEADLINE_SUB = "per month, fixed. GST as applicable."
FEE_TOTAL_LINE = "Rs 6,00,000 for the 90-day engagement"

FEE_COVERS = (
    "The fee is one fixed monthly charge, not a per-session or per-participant rate, so the cost "
    "is known at the outset and does not rise as more people are nominated. It covers the diagnose "
    "stage, design and customisation of all twelve modules and the induction programme, "
    "facilitation, guides, materials and job aids, assessments, observation, records, monthly "
    "reporting and management reviews."
)

FEE_SIMPLE = (
    "One fixed monthly fee of Rs 2,00,000, GST as applicable, for the full ninety days. Nothing "
    "in the programme is charged per session, per module or per participant."
)

# ── 03 curriculum ───────────────────────────────────────────────────────────────
SEQUENCE_INTRO = (
    "The sequence runs from awareness to self, then to tools, inner capability, application, "
    "complexity, sustainability and finally multiplication. Three placements are deliberate."
)

SEQUENCE_LOGIC = [
    ("Professional presence early",
     "the patient judges before a word is spoken, and it is the quickest change to become "
     "visible, which earns the programme credibility for the harder work that follows."),
    ("Difficult situations late, resilience straight after",
     "de-escalation depends on active listening, emotional regulation and agreed standards "
     "already being in place. Teaching complaint handling first is the most common design error."),
    ("Supervisors after their teams, Train-the-Trainer last",
     "a supervisor cannot reinforce a standard they did not sit through. Trained staff returning "
     "to untrained supervisors regress."),
]

# module, focus, weeks, sessions   (sessions must sum to 39 across 12 modules)
MODULES = [
    ("M1  Foundation & Orientation",
     "Vision, values, patient rights, conduct, safety protocol, emergency situational awareness, escalation and incident reporting",
     "1", 3),
    ("M2  Professional Presence",
     "Grooming, bearing, punctuality, personality and professional image, workplace etiquette",
     "2", 2),
    ("M3  Communication Fundamentals",
     "Verbal and non-verbal, active listening, telephone etiquette, clarity under pressure",
     "2–3", 4),
    ("M4  Emotional Intelligence & Empathy",
     "Self-awareness, self-regulation, empathy enhancement sessions, patient dignity and privacy",
     "4", 3),
    ("M5  Patient Experience & Standards",
     "First impressions, guiding, proactive service, service excellence, managing expectations and delays",
     "5–6", 4),
    ("M6  The Patient Journey",
     "Enquiry to discharge, touchpoint by touchpoint, allocated by role",
     "6–7", 4),
    ("M7  Difficult Situations & Recovery",
     "Difficult news, complaints, service recovery, conflict resolution, de-escalation, crisis management",
     "7–9", 5),
    ("M8  Personal Effectiveness & Resilience",
     "Stress management, compassion fatigue, self-motivation, self-efficacy, priorities, accountability",
     "9", 2),
    ("M9  Teamwork & Coordination",
     "Handovers, internal-customer mindset, interdepartmental coordination, escalation discipline",
     "10", 3),
    ("M10  Leadership & Supervisory",
     "Huddles, coaching, feedback, conflict resolution, underperformance",
     "11–12", 4),
    ("M11  Train-the-Trainer",
     "Adult learning, facilitation, assessment, reinforcement",
     "12–13", 3),
    ("M12  Consolidation & Review",
     "Post-assessment, effectiveness dashboard, management review",
     "13", 2),
]

# short focus strings for the 2-page edition, where the column is half as wide
MODULES_SHORT = [
    ("M1  Foundation & Orientation", "Patient rights, safety protocol, emergency situational awareness", "1", 3),
    ("M2  Professional Presence", "Grooming, bearing, personality and image", "2", 2),
    ("M3  Communication Fundamentals", "Non-verbal, active listening, telephone etiquette", "2–3", 4),
    ("M4  Emotional Intelligence & Empathy", "Self-regulation, empathy sessions, dignity and privacy", "4", 3),
    ("M5  Patient Experience & Standards", "First impressions, proactive service, service excellence", "5–6", 4),
    ("M6  The Patient Journey", "Enquiry to discharge, touchpoint by touchpoint, by role", "6–7", 4),
    ("M7  Difficult Situations & Recovery", "Complaints, service recovery, conflict, crisis management", "7–9", 5),
    ("M8  Personal Effectiveness & Resilience", "Stress management, self-motivation, self-efficacy", "9", 2),
    ("M9  Teamwork & Coordination", "Handovers, interdepartmental coordination, escalation", "10", 3),
    ("M10  Leadership & Supervisory", "Huddles, coaching, feedback, conflict resolution", "11–12", 4),
    ("M11  Train-the-Trainer", "Adult learning, facilitation, assessment, reinforcement", "12–13", 3),
    ("M12  Consolidation & Review", "Post-assessment, dashboard, management review", "13", 2),
]

COHORT_NOTE = (
    "Weeks 1 to 10 run frontline and staff batches, with supervisors attending alongside their own "
    "teams rather than in a separate senior run. Weeks 11 and 12 take the supervisory and "
    "leadership cohort, Weeks 12 and 13 the internal-trainer group. Induction is built during "
    "Diagnose and Design and delivered to each new-joiner cohort as they arrive, so it is a "
    "standing track rather than a calendar week."
)

ALLOCATION_NOTE = (
    "Every group takes the foundation modules; M6 is allocated by role, M10 is for supervisors and "
    "department heads, M11 for the nominated internal trainers."
)

# ── 04 outcomes by role ─────────────────────────────────────────────────────────
# group, what they gain, what they keep
ROLES = [
    ("Front office and reception",
     "First-impression protocol, telephone discipline, enquiry handling, waiting-time communication",
     "Greeting and telephone aid, waiting-time wording, escalation flowchart"),
    ("Patient relations",
     "Empathy-led enquiry, complaint intake, service recovery, closing the loop with families",
     "Service-recovery card, complaint and closure log, rounding question set"),
    ("Billing and administration",
     "Explaining estimates without jargon, financial conversations with distressed families, dispute de-escalation",
     "Billing-explanation framework, estimate checklist, de-escalation steps"),
    ("Nursing and clinical support",
     "Bedside courtesy, explaining what happens next, dignity and privacy, handovers, compassion fatigue. Behavioural layer only",
     "Bedside card, dignity and privacy checklist, handover aid"),
    ("Housekeeping and facility",
     "Conduct in patient areas, permission before entering, discretion, escalating beyond role",
     "In-room conduct card, request-and-escalate wording, confidentiality card"),
    ("Security",
     "Firm but courteous authority, visitor control without confrontation, de-escalating grief and agitation",
     "De-escalation ladder, gate-side entry wording, incident escalation aid"),
    ("Supervisors and department heads",
     "Huddles, on-floor observation and coaching, feedback, conflict, underperformance",
     "Huddle template, observation checklists, feedback structure, coaching questions"),
    ("Managers and leadership",
     "Reading the dashboard, linking recurring complaints to capability gaps, governing the calendar",
     "Effectiveness dashboard, monthly review pack, gap-to-action framework"),
]

# one-line role summaries for the 2-page edition, where the full three-column table will not fit
ROLES_BRIEF = [
    ("Front office and reception",
     "first-impression protocol, telephone discipline, waiting-time communication"),
    ("Patient relations",
     "empathy-led enquiry, complaint intake, service recovery, closing the loop"),
    ("Billing and administration",
     "explaining estimates without jargon, financial conversations, dispute de-escalation"),
    ("Nursing and clinical support",
     "bedside courtesy, dignity and privacy, handovers, compassion fatigue"),
    ("Housekeeping and facility",
     "conduct in patient areas, permission before entering, discretion, escalation"),
    ("Security",
     "firm but courteous authority, visitor control, de-escalating grief and agitation"),
    ("Supervisors and department heads",
     "huddles, on-floor observation and coaching, feedback, underperformance"),
    ("Managers and leadership",
     "reading the dashboard, linking complaints to capability gaps, governing the calendar"),
]

# ── 05 approach and delivery ────────────────────────────────────────────────────
STAGES = [
    ("DIAGNOSE",
     "Management discussions, departmental inputs, employee observation, and review of anonymised feedback and complaints."),
    ("DESIGN",
     "Every module customised against the hospital's own policies, SOPs and service standards. Induction is built here."),
    ("DELIVER",
     "Facilitated four-hour sessions: concept, demonstration, practice and feedback, three days a week."),
    ("REINFORCE",
     "Job aids carried to the point of work, supervisor coaching, and short observation visits during live shifts."),
    ("MEASURE",
     "Assessment before and after, on-the-job observation, and monthly reporting to management."),
]

METHOD_NOTE = (
    "All training is built on the narrative of real experience and real incidents: hospital-based "
    "case studies, incident reports, patient-interaction simulations, role plays, scenario "
    "discussions, microlearning, on-the-job observation and coaching, with assessment before and "
    "after. Employees practise how to do it rather than simply being told."
)

SESSION_ANATOMY = (
    "A four-hour session allows a full cycle of concept, demonstration, practice and feedback, of "
    "which 105 minutes are structured practice and a further 25 minutes participant case work."
)

DELIVERABLES = [
    "Training Needs Analysis report by end of Week 2, competency and skill-gap framework in Week 3, and a training calendar the hospital can extend quarterly",
    "The induction programme and all twelve customised modules, with facilitator guides, participant materials and role-specific job aids",
    "Assessment and observation instruments in use from Week 1, consolidated in Week 3",
    "Attendance records, feedback analysis, monthly training reports, and corrective plans where a standard is not holding",
    "Management review presentations and a training effectiveness dashboard",
]

MEASUREMENT_LEVELS = [
    ("01", "PARTICIPATION AND REACTION", "Attendance, completion and participant feedback by batch and by module."),
    ("02", "KNOWLEDGE GAIN", "Assessment before and after each module, scored and reported by cohort."),
    ("03", "BEHAVIOURAL CHANGE", "On-the-job observation against the same checklists supervisors use on the floor."),
    ("04", "ORGANISATIONAL INDICATORS", "Complaint and feedback themes read alongside capability gaps."),
]

MEASUREMENT_CAVEAT = (
    "The fourth level depends on hospital-held complaint and feedback data, so improvement there "
    "cannot be attributed to training alone. We report movement rather than guarantee it."
)

# ── 06 what we need ─────────────────────────────────────────────────────────────
NEEDS = [
    "A single point of contact from HR or L&D, and confirmed batch nominations ahead of each module block",
    "Participants released for the full four hours, and a training room with projection for up to 30",
    "Access to anonymised patient-feedback and complaint themes for case studies, and permission for on-the-job observation",
    "Nominated subject-matter experts for clinical, statutory and policy content, plus the hospital's own SOPs and service standards",
    "The legal entity name and billing details for invoicing",
]

TERMS = [
    "Invoices are raised monthly in arrears. GST as applicable.",
    "The calendar is confirmed jointly before commencement, and sessions missed for hospital reasons are rescheduled within the engagement window where possible.",
    "Hospital data is treated as confidential.",
]

OUTCOME_STATEMENT = (
    "A programme of this kind supports more confident employees, a more consistent patient "
    "experience, better complaint handling and service recovery, improved teamwork, stronger "
    "accountability, more effective supervisors, and a culture of continuous learning."
)

CLOSING = (
    "We would welcome the chance to walk your team through this in person and to adjust the design "
    "in light of what you know about your own floors."
)

# ── condensations used only by the 2-page edition ───────────────────────────────
# The nine capabilities as a single run-in line. The deck gives them a card each; the two-pager
# cannot afford a grid, but the vocabulary still has to be on the page.
CAPABILITIES_LINE = (
    "What the programme builds: awareness and self-efficacy · personality and image · emotional "
    "intelligence and empathy enhancement · quality, service excellence and proactive service · "
    "service recovery, conflict resolution, incident reporting and crisis management · "
    "interdepartmental coordination and communication · resilience, self-motivation and stress "
    "management · brand awareness · forecasted thinking about daily operations."
)

# The two-pager is the deliberately less detailed artefact. These are shortened rather than
# shrunk, so the page stays readable instead of dropping to a type size nobody will read.
SEQUENCE_LOGIC_BRIEF = [
    ("Professional presence early",
     "the patient judges before a word is spoken."),
    ("Difficult situations late, resilience after",
     "de-escalation needs listening and regulation already in place."),
    ("Supervisors after their teams",
     "staff returning to untrained supervisors regress."),
]

FEE_COVERS_BRIEF = (
    "The fee covers the diagnose stage, design and customisation of all twelve modules and the "
    "induction programme, facilitation, guides, materials and job aids, assessments, observation, "
    "records, monthly reporting and management reviews."
)

METHOD_BRIEF = (
    "All training is built on the narrative of real experience and real incidents: hospital-based "
    "case studies, incident reports, patient-interaction simulations, role plays, scenario "
    "discussions and coaching, with assessment before and after. Of each four-hour session, 105 "
    "minutes are structured practice and a further 25 minutes participant case work."
)

MEASUREMENT_BRIEF = (
    "Effectiveness is reported at four levels: participation and reaction; knowledge gain through "
    "assessment before and after; behavioural change through on-the-job observation against the "
    "checklists supervisors use; and organisational indicators, which depend on hospital-held "
    "complaint and feedback data and are therefore reported as movement rather than guaranteed."
)

WHO_WE_ARE_BRIEF = (
    "Levitatte brings a founder with more than twenty-five years in behavioural, communication and "
    "service capability building, grounded in NLP and organisational behavioural psychology, with "
    "prior healthcare engagements at Fortis and Cloud9 Hospitals. Industry-specific knowledge of "
    "hospital floors shapes every module."
)


# ── integrity guards, run at import so a renderer can never emit a broken figure ─
def _check():
    assert sum(m[3] for m in MODULES) == 39, "module sessions must sum to 39"
    assert sum(m[3] for m in MODULES_SHORT) == 39, "short module sessions must sum to 39"
    assert len(MODULES) == len(MODULES_SHORT) == 12, "twelve modules"
    for a, b in zip(MODULES, MODULES_SHORT):
        assert a[0] == b[0] and a[2] == b[2] and a[3] == b[3], f"module drift: {a[0]}"
    assert len(ROLES) == 8, "eight role groups"
    assert len(PILLARS) == 9, "nine capability pillars"
    assert len(STAGES) == 5, "five stages"


_check()
