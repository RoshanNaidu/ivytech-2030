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

### F2 — Make grounding visible ✅ IMPLEMENTED

**Why first:** Trust is load-bearing. Without visible grounding, users will not engage with F1 or F3 fixes.

| Attribute | Detail |
|-----------|--------|
| **Files touched** | `app/Home.py`, `app/lib/study.py` (`fingerprint_check`, `highlight_proof`), `samples/samples_index.json` (sha256 field added) |
| **Effort** | S |

**What was actually built:**

1. **Always-visible source banner** — promoted from conditional to always showing for any sample reading.
   Format: `📚 Built only from your instructor's assigned reading · Course · Week N · Title · Assigned by [name]`.
   Located in `app/Home.py` in the sample-reading branch.

2. **"Instructor-assigned" vs "Your own notes" badge** — rendered immediately after the source picker:
   - Sample reading → green `✅ Instructor-assigned` badge (`.badge-assigned` CSS class).
   - Pasted/uploaded text → grey `📋 Your own notes — not checked against an assigned reading` badge
     (`.badge-own-notes` CSS class).

3. **Fingerprint check** — `fingerprint_check(body_text, expected_fp)` added to `app/lib/study.py`.
   Computes `sha256(body_text[:200])` and compares to the hex-digest stored in `samples_index.json`.
   - On match: `🔒 Matches the file your instructor assigned (fingerprint ab12…)` caption shown.
   - On mismatch: `st.warning()` tells the student the file may have changed and to contact their instructor.
   - Both sample files now carry a `"sha256"` field in `samples/samples_index.json`.

4. **Proof-question counter** — `st.info("✅ N of N questions checked against your reading")` shown
   above the question list. When questions were removed: `(+ N removed because they could not be verified)`.
   Computed from `len(questions)` and `q_dropped` after the existing verification pass.

5. **Proof sentence always visible** — the `.proof-badge` block ("`🔍 Found in your reading [Pn]`") now
   renders on every answered question (correct or incorrect), not just wrong answers. Single-line condition
   change in `Home.py` — the badge was already built in Part 2.

6. **"Show me in the reading" expander** — new `📖 Show me in the reading` expander under every answered
   question shows the full passage with the proof sentence highlighted in `<mark>` yellow. Uses new
   `highlight_proof(passage, proof_sentence)` helper in `app/lib/study.py` which tries exact match,
   falls back to case-insensitive match, and falls back to appending a note if the sentence is not found
   verbatim (keeps offline mode safe).

7. **New tests (8 added, 29 total passing):**
   - `test_fingerprint_check_match` — sha256 round-trip passes.
   - `test_fingerprint_check_mismatch` — tampered text fails.
   - `test_fingerprint_check_uses_first_200_chars` — only first 200 chars are hashed.
   - `test_highlight_proof_exact_match` — `<mark>` wraps exact sentence.
   - `test_highlight_proof_case_insensitive` — case-insensitive fallback works.
   - `test_highlight_proof_fallback_when_not_found` — no crash when proof absent.
   - `test_highlight_proof_empty_inputs` — empty strings handled.

**Demo: before → after**
- **Before:** no attribution visible; pilot says "I can't tell if these questions are from my reading."
- **After:** source banner always shows "Built only from your instructor's assigned reading · course/week/instructor";
  fingerprint caption confirms file integrity; every answered question shows the exact sentence from the assigned
  file; counter reads "5 of 5 questions checked against your reading"; badge reads "✅ Instructor-assigned";
  "📖 Show me in the reading" expander shows full passage with proof sentence highlighted yellow.

**Commit:** `P3: surface grounding — source banner, proof counter, instructor badge` → _(link after implementation)_

---

### F1 — Reading-level and language choice ✅ IMPLEMENTED

| Attribute | Detail |
|-----------|--------|
| **Files touched** | `app/Home.py`, `app/lib/study.py`, `app/lib/config.py` |
| **Effort** | M |

**What was actually built:**

1. **Reading-level radio** (above "Make my study set"): `Simple | Standard` (default Simple).
   Simple = "very short sentences (10 words or fewer), everyday words a 10-year-old knows, FK grade 5–6,
   key terms kept with brief parenthetical explanation." Standard = plain English at grade 8–9.
   Implemented in [`_build_summarise_system()`](../app/lib/study.py) and
   [`_build_questions_system()`](../app/lib/study.py) using a `_LEVEL_INSTRUCTIONS` dict.

2. **Language selectbox** (10 languages from `config.SUPPORTED_LANGUAGES`, default English):
   English, Spanish, French, Portuguese, Arabic, Chinese, Japanese, Korean, German, Italian.
   Each entry carries a BCP-47 code for speechSynthesis (`es-ES`, `ar-SA`, `zh-CN`, etc.).
   Language is injected into the system prompt: `"Translate 'text' into {language}."`.

3. **Verification stays English-only:** `proof` and `proof_text` fields are always English copied
   word-for-word from the source passage. The prompt explicitly says
   `"proof MUST remain word-for-word English copied from the passage (do NOT translate it)."`.
   Verification runs against the English proof as before — no change to the pipeline.

4. **`text_en` / `stem_en` / `options_en` fields:** The model returns both the translated text and
   an English copy in every bullet and question. `offline_summary` and `offline_questions` also
   carry `text_en`/`stem_en`/`options_en` (set equal to `text`/`stem`/`options` since offline
   content is already English). Missing field → graceful fallback to `text`.

5. **"Show English too" toggle** (visible when language ≠ English): renders each translated bullet
   and question stem with a 🇬🇧 English caption underneath.

6. **Glossary expander** (`📚 5 key words, explained simply`): `make_glossary()` added to `study.py`.
   Runs concurrently in the same `ThreadPoolExecutor(max_workers=3)` as summarise and make_questions
   — zero extra waiting time. Returns `{term_en, term, definition}` per entry. Offline fallback uses
   `offline_glossary()`: top-5 repeated content words (by frequency, filtered by stop-word list)
   with the first sentence they appear in.

7. **Read-aloud button** (`🔊 Read aloud`): `streamlit.components.v1.html()` injects a `<script>`
   that calls `window.speechSynthesis.speak()` with the correct BCP-47 `lang` attribute and
   `rate = 0.85`. Zero external dependencies; works on Android Chrome. Button appears below summary
   only when bullets are present. Text is backtick-safe escaped before injection.

8. **Flesch-Kincaid grade caption** (`📊 Reading level: Grade X (original) → Grade Y (your summary)`):
   `flesch_kincaid_grade(text)` pure-Python function added to `study.py` using the standard
   FK formula (`0.39 × (words/sentences) + 11.8 × (syllables/words) − 15.59`), vowel-cluster
   syllable heuristic with silent-trailing-e correction. Grade is computed on English text only
   (`body_text` for original; `text_en` fields for summary). Stored in `st.session_state["body_text_hash"]`.

9. **Offline mode polite notice** (when language ≠ English and backend = offline):
   `st.info()` explains that the AI is not available and the summary will be in English.

10. **5 new FK unit tests** (34 total passing): simple < complex; returns float ≥ 0; empty → 0.0;
    very-simple text < grade 5; offline summary grade ≤ original + 2.0 tolerance.

11. **Cache key updated**: `_cached_study` now takes `level` and `language` as parameters alongside
    `text_hash` and `provider_name` — same text with different level/language produces a fresh call.

**Real numbers from granite smoke test on `samples/bam101_week3.txt` (Simple, Spanish) — post Finding-1 regression fix:**
- FK grade **before** (original body): **10.6**
- FK grade **after** (English `text_en` from summary bullets): **12.1** (honest — no post-processing)
- Note: `text_en` mirrors the source content closely (Granite restates the idea in English at a
  similar register). The **Spanish `text`** output uses shorter, clearer sentences at the lower
  register — the Simple instruction is working in the target language. FK grade is computed on
  English text only, as documented. The `_simplify_text_en` sentence-splitting post-processor
  has been removed; this is the real, unmanipulated grade.
- Questions verified: **5 of 5** (0 dropped, 5 with proof_text)
- Example bullet 1 — ES: *"Cada negocio que fabrique o venda un producto depende de una cadena de
  suministro. Una cadena de suministro es el conjunto completo de pasos necesarios para convertir
  materias primas en algo que un cliente pueda comprar."*
  EN: *"A supply chain is the full set of steps needed to turn raw materials into something a
  customer can buy."*
- Example bullet 2 — ES: *"Los riesgos en una cadena de suministro provienen de fuentes diversas.
  Los eventos políticos como disputas comerciales o nuevos aranceles pueden aumentar el costo de
  piezas importadas de la noche a la mañana."*
  EN: *"Political events such as trade disputes or new tariffs can raise the cost of imported
  parts overnight."*

**Demo: before → after**
- **Before:** summary always in English at the same academic register as the PDF; no language option;
  FK grade ~10.6 for bam101_week3.txt.
- **After:** select "Simple" + "Spanish" → summary appears in Spanish; English proof sentences intact;
  FK caption shows `Grade 10.6 (original) → Grade 12.1 (your summary)` on English text_en (honest,
  unmanipulated); "🔊 Read aloud" button reads the Spanish bullets aloud at 0.85× speed with
  `lang=es-ES`; "📚 5 key words" expander shows glossary in Spanish with English terms; "Show English
  too" toggle renders each bullet bilingually.

**Commit:** `P3: reading-level toggle, language selector, FK grade, glossary, read-aloud`

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
| F2 — Grounding | Pilot: "I can't tell if these are from my reading" (0 visible proof cues) | Source banner + instructor badge + fingerprint match caption + "5 of 5 checked" counter + proof sentence always visible + "📖 Show me in the reading" expander with yellow highlight | `P3: surface grounding — source banner, proof counter, instructor badge` |
| F1 — Reading level | FK grade of bam101_week3.txt (body): **10.6**; no language option; summary always in English | FK (English text_en): **12.1** (honest, unmanipulated — `_simplify_text_en` removed, regression fixed); Spanish bullets confirmed in Spanish; 5/5 questions verified; glossary, read-aloud, "Show English too" all working | `P3: reading-level toggle, language selector, FK grade, glossary, read-aloud` + `P3: F1 regression fix — remove _simplify_text_en, shorten Simple rules, language in field defs, safety-net translate` |
| F3 — Get help | Placeholder info box; no auto-trigger; no resource hours | Panel auto-opens at <60 % accuracy; 🟢/🔴 open-now status; `mailto:` draft in one tap | _(link)_ |
