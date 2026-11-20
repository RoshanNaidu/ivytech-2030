# Pilot Feedback — Phase 3
## StudyBuddy · Ivy Tech IT Challenge 2026 · Case 2: Alternative-Format Study Tool

---

## 1 · Three Findings (verbatim) and Lena's Persona Impact

### Finding 1
> **"The summaries are still difficult to understand. Let me choose a simpler reading level or another language."**

**Persona impact for Lena.**
Lena studies 11 pm–1 am after a full workday. Spanish is her first language; dense academic English slows her
down and costs minutes she does not have. If the AI summary comes back at the same academic register as the
original PDF — with long clauses, discipline jargon, and passive constructions — she gains nothing. She reads
it three times, stays uncertain whether she understood, and goes to bed without confidence for Thursday's quiz.
A reading-level toggle and a language option are not "nice to have" for Lena; they are the difference between
the tool working for her and not working at all.

---

### Finding 2
> **"I cannot tell whether the practice questions are based on the material my instructor actually assigned."**

**Persona impact for Lena.**
Lena uses the tool as a bridge to the graded quiz. If she suspects the questions are hallucinated or pulled from
outside her assigned reading, the practice is worthless — worse than worthless, it may build false confidence
about content that will not appear on the quiz, or miss content that will. Trust is the product: if she cannot
see that every question comes from a specific sentence in the file her instructor assigned, she will stop using
the tool. As an ESL learner navigating academic literacy in English, she cannot afford to second-guess whether
the study material is legitimate.

---

### Finding 3
> **"When I am still stuck, I need an easy way to find a tutor or ask a real person for help."**

**Persona impact for Lena.**
Every human support resource at Ivy Tech closes by 9 pm. Lena studies after 11 pm. The tutoring centre, the
writing centre, her instructor's office hours — all unavailable in her study window. The Phase 2 prototype has
a placeholder panel that says "In the full version a prefilled form would open here." That is not a path to a
person; it is a dead end. When she scores below 60 % on practice questions, or hits a concept she still does
not understand after checking the proof sentence, she needs to know exactly who to contact, whether they are
reachable right now, and to be able to draft a message without starting from a blank subject line at midnight.

---

## 2 · Smallest Changes to the Existing Build

### F2 — Make grounding visible (implement first)

**Why first:** Trust is load-bearing. Without visible grounding, users will not engage with F1 or F3 fixes.

| Attribute | Detail |
|-----------|--------|
| **Files touched** | `app/Home.py`, `app/lib/config.py` (new `ASSIGNED_READINGS` list) |
| **Effort** | S |

**Changes:**

1. **Source banner** (already CSS-defined in Home.py as `.source-banner`; promote it to always-visible, not
   just for sample readings). Banner format: `📚 Course · Week N · Title · Assigned by [name]`.
2. **"Instructor-assigned" vs "Your own notes" badge** on the section header:
   - Sample reading → green `✅ Instructor-assigned` badge.
   - Pasted text → grey `📋 Your own notes` badge.
3. **Fingerprint check** in [`app/Home.py`](../app/Home.py): when a sample is loaded, compute
   `sha256(body_text[:200])` at page-load and compare it to the hash stored in `samples_index.json`;
   show a one-line warning if the content has changed.
4. **Proof-question counter** `"N of N questions checked against your reading"` displayed above the
   question list, computed from `len(questions)` after the existing verification pass in
   [`app/lib/study.py`](../app/lib/study.py).
5. **Exact proof sentence per question** is already built in Part 2
   (`proof_text` field surfaced via the `.proof-badge` CSS block). Keep it; ensure it renders on
   every answered question, not only on wrong answers — a one-line condition change in `Home.py`.

**Demo: before → after**
- **Before:** no attribution visible; pilot says "I can't tell if these questions are from my reading."
- **After:** source banner always shows course/week/instructor; every question shows the exact sentence from
  the assigned file; counter reads e.g. "5 of 5 questions checked against your reading"; badge reads
  "✅ Instructor-assigned".

**Commit:** `P3: surface grounding — source banner, proof counter, instructor badge` → _(link after implementation)_

---

### F1 — Reading-level and language choice (implement second)

| Attribute | Detail |
|-----------|--------|
| **Files touched** | `app/Home.py` (UI controls + prompt parameter passing), `app/lib/study.py` (prompt injection), `app/lib/config.py` (supported languages list) |
| **Effort** | M |

**Changes:**

1. **Reading-level toggle** (above "Make my study set"): `Simple (Grade 5–6) | Standard (Grade 8–9)`.
   The chosen level is injected into the system prompt in
   [`_SUMMARISE_SYSTEM`](../app/lib/study.py:250) and [`_QUESTIONS_SYSTEM`](../app/lib/study.py:263):
   `"Use a {level} reading level."`.
2. **Language selector** (dropdown, default "English"). Supported languages drawn from
   `config.SUPPORTED_LANGUAGES` — limited to the ten languages IBM Granite 3.3 supports:
   English, Spanish, French, Portuguese, Arabic, Chinese, Japanese, Korean, German, Italian.
   Chosen language injected into the system prompt: `"Respond in {language}."`.
3. **"Show English too" toggle** (appears only when a non-English language is selected). When on,
   each summary bullet renders both the translated text and the original English proof sentence
   (proof sentences always stay in English, since they are copied verbatim from the source).
4. **5-word glossary panel** (small expander below the summary): `ask()` called with a one-sentence prompt
   `"List the 5 hardest vocabulary words in this reading and define each in one simple sentence."` Results
   cached in session state alongside the study set so it costs zero extra calls on re-render.
5. **Read-aloud button** (`🔊 Read aloud`) below the summary section. Uses the browser's
   `window.speechSynthesis` API via an `st.components.v1.html()` snippet — zero external dependencies,
   works on Android Chrome. Button triggers JS: `speechSynthesis.speak(new SpeechSynthesisUtterance(text))`.
6. **Flesch-Kincaid grade display** (caption below the summary): computed in Python using the standard
   FK formula (`0.39 × (words/sentences) + 11.8 × (syllables/words) − 15.59`), implemented as a 10-line
   pure-Python function in [`app/lib/study.py`](../app/lib/study.py). Shows:
   `Reading level: Grade 10.2 → Grade 6.4` (before = original text grade; after = summary grade).

**Demo: before → after**
- **Before:** summary at the same register as the PDF; no language option; Flesch-Kincaid grade ~10–12
  for a typical supply-chain text.
- **After:** toggle to "Simple", select "Spanish" → summary appears in Spanish at grade 5–6; English proof
  sentences remain intact; Flesch-Kincaid caption shows e.g. `Grade 11.4 → Grade 5.8`; "🔊 Read aloud"
  reads the bullets aloud.

**Commit:** `P3: reading-level toggle, language selector, FK grade, glossary, read-aloud` → _(link after implementation)_

---

### F3 — "Get help from a person" panel (implement third)

| Attribute | Detail |
|-----------|--------|
| **Files touched** | `app/Home.py` (panel logic, trigger conditions, mailto link), `app/lib/config.py` (new `HELP_RESOURCES` list with hours) |
| **Effort** | M |

**Changes:**

1. **`HELP_RESOURCES` in `config.py`** — a list of dicts:
   ```python
   HELP_RESOURCES = [
       # SAMPLE DATA — confirm names, emails, and hours with Ivy Tech before final demo
       {"name": "Learning Resource Center", "type": "tutoring",
        "hours": "Mon–Thu 8 am–8 pm, Fri 8 am–5 pm", "email": "lrc@ivytech.edu"},
       {"name": "Writing Center",           "type": "writing",
        "hours": "Mon–Fri 9 am–7 pm",                 "email": "writing@ivytech.edu"},
       {"name": "Instructor (via portal)",  "type": "instructor",
        "hours": "Responds within 24 hours",           "email": ""},
   ]
   ```
   Labelled prominently as **sample data** until confirmed with Ivy Tech.

2. **"Open right now" logic** in `Home.py`: compare `datetime.now()` to each resource's hours string;
   show a 🟢 / 🔴 indicator. Pure Python, no external library.

3. **Automatic trigger** — the panel opens automatically (using `st.session_state`) when:
   - Accuracy drops below 60 % after at least one question checked, OR
   - User taps a new **"I'm still stuck"** button that appears below each incorrect answer.

4. **"Draft a message to my instructor" subpanel** — when the user taps it:
   - `ask()` generates a short, polite message draft containing: course name, week, the question she
     is stuck on, and one line summarising what she tried.
   - Draft rendered in an editable `st.text_area`.
   - A `mailto:` link (HTML anchor) lets her open the draft in her phone's email client with one tap.
   - The app stores nothing, sends nothing, and the footer caption says so explicitly.

5. **Replace Phase 2 placeholder** — remove the `"In the full version…"` info box; replace it with
   the real panel described above.

**Demo: before → after**
- **Before:** dummy expander with static text "not sent anywhere"; no auto-trigger; no open/closed status.
- **After:** score falls to 40 % → panel opens automatically showing which resources are open right now;
  user taps "I'm still stuck" on Q3 → panel highlights; taps "Draft a message" → AI writes a draft;
  user copies or taps the `mailto:` link; nothing is stored.

**Commit:** `P3: get-help panel — config resources, open-now indicator, auto-trigger, instructor draft` → _(link after implementation)_

---

## 3 · Implementation Order, Commits, and A-Ivy Principles

| Order | Finding | Commit message | A-Ivy principle |
|-------|---------|---------------|-----------------|
| 1 | **F2** — Grounding visible | `P3: surface grounding — source banner, proof counter, instructor badge` | **Ground answers in approved sources.** Every study item is traceable to the sentence in the file the instructor assigned. |
| 2 | **F1** — Reading level & language | `P3: reading-level toggle, language selector, FK grade, glossary, read-aloud` | **Design for accessibility.** The tool adapts to Lena's language and literacy level; it does not demand she adapt to it. |
| 3 | **F3** — Get help from a person | `P3: get-help panel — config resources, open-now indicator, auto-trigger, instructor draft` | **Give users a path to a human.** The AI handles what it can and explicitly routes harder questions to a real person at the right moment. |

Each finding is one commit. The commit history shows all three addressed within the existing build, with
no restart.

---

## 4 · Not Changed, and Why

| What we did NOT change | Reason |
|------------------------|--------|
| **`app/lib/study.py` verification logic** | The fuzzy-match pipeline already corrects wrong `passage_id` values and drops unverifiable items. F2 makes the results of this pipeline visible to the user; it does not need to change how the pipeline works. |
| **`app/lib/ai.py` and the AI backend** | Language and level are injected as prompt text. No backend change is needed; Granite 3.3 handles all ten supported languages natively. |
| **The offline fallback path** | Offline bullets come from the first sentence of each passage. For F1, the FK grade will reflect the original sentence (grade ~8), which is still informative. Adding offline translation would require a local translation model beyond challenge scope. |
| **The stats / metrics row** | The night-sets counter and accuracy metric already serve as the prototype's leading-indicator evidence. No change needed for Part 3. |
| **Any new page or route** | All three fixes land in `app/Home.py` and `app/lib/config.py`. Adding a new page would fragment the mobile single-screen experience Lena relies on. |
| **Student data handling** | No names, IDs, or quiz scores are stored or sent anywhere. This was correct in Part 2 and is kept correct here; the "Draft a message" feature uses a `mailto:` link so the app never touches the message after rendering it. |

---

## 5 · Before → After Evidence _(fill in after implementation)_

| Finding | Before (measurable) | After (measurable) | Commit |
|---------|--------------------|--------------------|--------|
| F2 — Grounding | Pilot: "I can't tell if these are from my reading" (0 visible proof cues) | Source banner + instructor badge + "5 of 5 checked" counter + proof sentence always visible | _(link)_ |
| F1 — Reading level | Flesch-Kincaid grade of bam101_week3.txt summary: _(fill after build)_ | Grade after "Simple" toggle: _(fill after build)_; Spanish output verified on screen | _(link)_ |
| F3 — Get help | Placeholder info box; no auto-trigger; no resource hours | Panel auto-opens at <60 % accuracy; 🟢/🔴 open-now status; `mailto:` draft in one tap | _(link)_ |
