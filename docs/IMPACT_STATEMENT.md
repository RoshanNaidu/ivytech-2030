# 2030 Impact Statement: StudyBuddy

*One page. Every number is computed from challenge data or labelled as an assumption.*

**Pillar:** Academic & Instructional Quality — Ensure Consistent Quality Across Learning Modalities  
**Squad:** Innovation Squad · Roshan Naidu, Adesh Sanghera, MadFrank2006, jhershfi-cpu

---

## Who benefits

**Primary:** Online working-adult students like Lena — 27, ESL, phone-only, studying after 11 pm with no
access to human tutoring. Ivy Tech enrolls 215,000+ students statewide (2025–26); a large share of online
sections serve exactly this profile.

**Secondary:** Instructors gain a transparent audit trail (source banner, passage fingerprint, proof
sentences) showing what the AI told their students. Academic support staff see unresolved "get help"
requests in real time and can prioritize outreach. Employers gain graduates who complete rather than drop.

---

## Which metric improves, and by how much

| Metric | Baseline (source) | 2030 target | Change |
|--------|-------------------|-------------|--------|
| Online course completion rate | 62% *(ASSUMPTION — to confirm with Ivy Tech institutional data)* | 70% | +8 percentage points |

Every **1,000 online course enrollments** reached by StudyBuddy at +8 points means about **80 more completed
courses per term** (statewide online enrollment to be confirmed with Ivy Tech data) — each one a module, a credential, or a degree step closer for a student who would
otherwise have quietly dropped.

**Mechanism:** StudyBuddy removes the two most common drop triggers for students like Lena: not
understanding the reading, and not knowing whether they are ready for the quiz. Practice-question accuracy
on first attempt is our leading indicator — a rising score predicts quiz readiness before the graded
assessment, giving students time to go back to the right page rather than drop the course.

---

## What a statewide rollout would take

1. **Pilot (Spring 2027):** One fully online course (100–200 students) at one campus. Measure
   completion rate and practice-question accuracy against the same course in the prior term.
   Cost: minimal — Ollama + Granite 3.3 8B runs on a single server or a faculty laptop.

2. **LMS integration (Fall 2027):** Embed StudyBuddy inside Ivy Tech's learning management system via LTI.
   Connect the "Get help from a person" button to the existing tutoring ticketing system.
   Estimated staff time: 2–3 FTE months (IT + instructional design). No new data left the campus
   boundary; all inference stays on campus-hosted hardware.

3. **Statewide scale (2028–2030):** Deploy campus-hosted Granite nodes at all 19 campuses.
   Each campus IT team runs Ollama; no cloud API keys, no per-query cost, no FERPA exposure.
   Success criterion to continue: completion rate in treated sections ≥ 2 points above control
   after two consecutive terms.

---

## Top risk and how we mitigate it

**Risk: AI inaccuracy and student over-reliance.** A student trusts a hallucinated summary, fails
the quiz, and loses confidence — the opposite of the intended effect. At scale, systematic errors
could widen equity gaps rather than close them.

**Mitigations:**
- **Passage-grounded generation only.** The model receives the instructor-assigned text as its sole
  context; it cannot draw on outside knowledge for the summary or practice questions.
- **Proof sentence displayed on every answer.** The exact sentence from the reading that supports
  each answer is shown to the student, so they can verify — and to the instructor, who can flag errors.
- **"N of N questions checked" counter.** Students see how many answers passed the grounding check
  before they practice.
- **F3 human-help path.** Any question the AI cannot ground routes directly to a human tutor.
- **Leading-indicator monitoring.** Practice-question accuracy is tracked per session (no PII).
  A drop in accuracy triggers instructor review before the graded quiz.

**Signal we watch:** If pilot practice-question accuracy falls below 75% on first attempt, we pause
and audit the grounding pipeline before expanding to additional courses.
