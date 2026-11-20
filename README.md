# Ivy Tech 2030: StudyBuddy

> **IT Challenge 2026: Data Analytics, Applied AI & Informatics.** *The Future of Ivy Tech: Build the 2030
> Experience with IBM Bob.* An Innovation Squad prototype for one pillar of Ivy Tech's Strategic Plan 2030.

**Pillar:** Academic & Instructional Quality · **For:** Lena (online working adult, ESL, phone-only, 11 pm–1 am) · **2030 outcome:** Online course completion rate from 62% → 70%

<!-- Screenshot or GIF of the core flow goes here: docs/img/demo.png -->

## Problem

Lena Trujillo *(fictional — see [`docs/PERSONA.md`](docs/PERSONA.md))* is 27, works full-time, parents alone
after 8 pm, and studies on her Android phone between 11 pm and 1 am. Her course reading is a dense academic
PDF. The textbook chatbot returns jargon with no glossary. The tutoring center closed at 8 pm. She goes to bed
uncertain whether she is ready for Thursday's quiz. If that uncertainty persists week after week, she drops.
Ivy Tech's online completion rate sits at approximately 62% (ASSUMPTION — to confirm with Ivy Tech data);
every student like Lena who quietly falls behind moves that number down.

## Solution

**StudyBuddy** turns an instructor-assigned reading into a plain-language summary and verified practice
questions — all grounded in the passage, all on her phone, in under two minutes.

- **F2 — Visible grounding (pilot update):** Every summary carries an instructor-assigned banner showing
  the source, a passage fingerprint, a "N of N questions checked" count, and an exact proof sentence
  pulled from the reading. Students and instructors can see exactly where each claim comes from.
- **F1 — Reading accessibility:** Summaries are rewritten to a lower reading level and offered in 10
  languages with a one-tap English toggle, an inline glossary, read-aloud (TTS), and a readability grade
  displayed on screen.
- **F3 — Human-help path:** A "Get help from a person" button routes Lena to a live tutor or academic
  support resource. Full routing is planned / in progress; the entry point is live.

## AI & technical approach

- **App:** Python 3.12 + Streamlit multipage app (`app/`), Plotly charts, pandas.
- **AI model:** IBM Granite 3.3 8B, run locally via [Ollama](https://ollama.com) (`AI_PROVIDER=granite`).
  Passage-grounded generation: the model receives only the instructor-assigned text as context; every
  answer is verified against the source before display. Claude and an offline fallback are also supported.
- **Proof verification:** After generation, `app/lib/ai.py` checks each practice-question answer against
  the source passage and surfaces the exact supporting sentence — the F2 "proof sentence" Lena and her
  instructor can read.
- **Privacy:** No student names or IDs enter any prompt or log. All inference runs on-device (Granite/Ollama).
- **Quality:** smoke tests (`uv run pytest -q`), lint (`uv run ruff check app tests`), GitHub Actions CI on every push.

## Pillar & statewide strategy

**Pillar:** Academic & Instructional Quality — *Ensure Consistent Quality Across Learning Modalities*
([Ivy Tech Strategic Plan 2030](https://www.ivytech.edu/strategicplan)).

StudyBuddy advances this pillar through the **A-Ivy** principle: AI supports people, stays grounded in
instructor-approved sources, and always provides a path to a human.

| A-Ivy principle | StudyBuddy feature |
|---|---|
| Grounded in approved sources | Instructor-assigned banner + passage fingerprint (F2) |
| Plain language for every learner | Reading level rewrite, 10 languages, glossary, TTS (F1) |
| AI assists, humans decide | "Get help from a person" routing to live tutor (F3) |
| No data leaving the device | Granite 3.3 8B via Ollama, fully local inference |
| Transparent to instructors | "N of N questions checked" + exact proof sentence (F2) |

## How we used IBM Bob

IBM Bob was our core development tool across all four challenge phases. Full session log: [`docs/BOB_LOG.md`](docs/BOB_LOG.md).

- **Plan mode:** Problem framing, persona development, pillar mapping, and metric selection.
- **Agent mode (Bob Shell):** Scaffolded the Streamlit app, wrote `app/lib/` helpers, built F1 and F2
  features, and generated tests — all from plain-language prompts.
- **Custom Pilot Feedback mode** ([`.bob/custom_modes.yaml`](.bob/custom_modes.yaml)): Structured our
  post-pilot review; Bob identified the grounding gap that became the F2 visible-grounding update.

## Impact

See the one-page [2030 Impact Statement](docs/IMPACT_STATEMENT.md) and [pilot feedback](docs/PILOT_FEEDBACK.md).

## Run it

```bash
./scripts/setup.sh                      # installs uv + Python 3.12 + dependencies
uv run streamlit run app/Home.py        # http://localhost:8501
uv run pytest -q                        # tests
```

Optional AI: copy `.env.example` to `.env` and set `AI_PROVIDER` (`granite` with Ollama for local IBM Granite 3.3 8B, `claude` + key, or `offline`).

## Team

| Member | Role | Main contributions |
|--------|------|--------------------|
| Roshan Naidu | Lead / PM | Ran IBM Bob (Bob Shell) for all build phases, reviewed and tested output, demo |
| Adesh Sanghera | Team member | Persona review, pilot feedback, demo |
| MadFrank2006 | Team member | Ran IBM Bob for all build phases but focused primarily on the front end development, persona creation, and developing a clear and actionable plan.  |
| jhershfi-cpu | Team member | Impact story, demo |

## Repository map

```
app/Home.py, app/pages/   Streamlit screens
app/lib/                  config (problem framing), data, ml, charts, ai, ui helpers
data/                     challenge data (git-ignored)
docs/                     Impact Statement, Bob log, user stories, pilot feedback, demo script, playbook
.bob/, AGENTS.md          IBM Bob rules, custom modes and project context
```

## Preparation disclosure

Before the event we prepared only reusable tooling: this generic Streamlit starter (data loading, charts,
baseline model, AI wrapper), documentation templates and IBM Bob configuration. The problem, analysis and
prototype were defined and built during the challenge with IBM Bob; see the commit history and Bob log.
