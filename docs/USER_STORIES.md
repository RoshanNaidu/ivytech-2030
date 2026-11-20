# User Stories — Alternative-Format Study Tool

**Persona:** Lena Trujillo *(fictional)* — 27-year-old online student, accounts-payable clerk by day,
single phone, studies 11 pm–1 am, English as a second language. See [`docs/PERSONA.md`](PERSONA.md)
for her full story.

---

## Stories

| # | Story | Acceptance criteria | Priority | Status |
|---|-------|---------------------|----------|--------|
| 1 | As an online student, I can turn a course reading into a plain-language summary so that I understand the key ideas even when academic English is hard for me. | **Given** I paste or type a course reading into the study screen **When** I tap "Summarise" **Then** I see 3–5 bullet points in plain language, each one labelled with the passage it came from (e.g. P2), and I can tap the label to jump back to the original text. | **MVP** | ☐ |
| 2 | As an online student, I can answer practice questions drawn from the reading so that I know whether I am ready for the quiz before I go to sleep. | **Given** a summary has been generated **When** I tap "Practice" **Then** I see 3 multiple-choice questions, each citing its passage id; I select an answer, see whether I was right, and see the exact sentence from the reading that proves the answer. No question appears if its answer text cannot be found in the source passage. | **MVP** | ☐ |
| 3 | As an online student studying on a phone at night, I see a dark-themed, single-scroll screen with large readable text so that the app does not hurt my eyes or require a laptop. | **Given** I open the app on a phone **When** the page loads **Then** the background is dark, body text is at least 16 px, and the entire flow fits in one vertical scroll with no horizontal scroll. | **MVP** | ☐ |
| 4 | As an online student, I can request help from a human tutor when the AI cannot answer my question so that I am never stuck with no path forward. | **Given** I am on the study screen **When** I tap "Ask a person" **Then** a prefilled message form opens (course name, week, and my question pre-populated) and a note appears explaining that a tutor will respond by the next business day. No PII is stored by the prototype; the form is a UI demo only in Phase 2. | **Next** | ☐ |
| 5 | As an online student who prefers Spanish, I can toggle the summary and questions into Spanish so that I spend less time translating and more time learning. | **Given** a summary has been generated **When** I tap the "ES" language toggle **Then** all summary bullets and question text re-render in Spanish while the original English passage labels are preserved for citation. | **Next** | ☐ |

---

## Acceptance criteria detail

### Story 1 — Summarise (MVP)
```
Given: I have pasted a reading of at least 100 words into the text area
  and I have selected a course name and week number
When: I tap "Summarise"
Then: a summary section appears with 3–5 bullets
  and each bullet ends with a [Px] passage citation
  and each cited passage exists in the split reading
  and bullets whose source text cannot be verified are not shown
  and the app works in offline mode (shows a deterministic fallback summary)
```

### Story 2 — Practice questions (MVP)
```
Given: a summary is displayed
When: I tap "Practice"
Then: 3 multiple-choice questions appear
  and each question ends with [Px]
  and after I choose an answer, the correct passage text is shown
  and no question is shown whose answer text does not appear in the named passage
  and my accuracy (correct / total attempted) is tracked in session state
```

### Story 3 — Mobile dark UI (MVP)
```
Given: the page is opened in a mobile browser or narrow viewport
When: any part of the study flow is displayed
Then: background colour is dark (hex #0e1117 or equivalent)
  and all body text is >= 16 px
  and no horizontal scroll appears at 390 px viewport width
  and the page title, text area, Summarise button, and Practice section
      are all reachable by vertical scroll only
```

### Story 4 — Get help from a person (Next)
```
Given: I am on the study screen
When: I tap "Ask a person"
Then: a modal opens pre-filled with course name, week, and an editable question field
  and a "Send" button is visible
  and tapping "Send" shows a confirmation: "Your question has been noted.
      A tutor will respond by the next business day."
  and no data is written to any database in the Phase 2 prototype
```

### Story 5 — Language toggle (Next)
```
Given: a summary and questions are displayed in English
When: I tap the "ES" toggle
Then: summary bullets re-render in Spanish
  and practice question text re-renders in Spanish
  and passage labels [Px] remain unchanged
  and an "EN" toggle returns to English without re-calling the AI
```

---

## Measurable 2030 outcome

Online course completion rate from **~62 %** (assumed current baseline, to be confirmed with
provided data on challenge day) to **≥ 70 %** by 2030, measured by Ivy Tech's semester-end
completion records for online sections.

*Leading indicators the prototype tracks in-session (no PII stored):*
- Study sets created 9 pm – 6 am (engagement in real study window)
- Practice-question accuracy on first attempt (quiz-readiness proxy)
- "Get help from a person" taps (A-Ivy human-escalation guardrail)
