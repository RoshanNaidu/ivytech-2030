"""StudyBuddy — Home screen.

Mobile-first study tool for Lena: paste or upload a course reading,
get a plain-language summary and practice questions, check every answer
against the source passage.

Layout follows the wireframe in docs/BUILD_PLAN.md.
"""

from __future__ import annotations

import json
import pathlib
from typing import Any

import streamlit as st
import streamlit.components.v1 as components

from lib import config
from lib.ai import ask
from lib.study import (
    fingerprint_check,
    flesch_kincaid_grade,
    highlight_proof,
    make_glossary,
    make_questions,
    split_passages,
    strip_metadata,
    summarise,
)
from lib.ui import page

# ── Page chrome ──────────────────────────────────────────────────────────────
page("Study", icon="📖")

# ── Mobile-friendly CSS ───────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Minimum 16 px body font; large tap targets */
    html, body, [class*="css"] { font-size: 16px !important; }
    .stButton > button {
        font-size: 1.1rem !important;
        padding: 0.6rem 1.2rem !important;
        border-radius: 8px !important;
        width: 100%;
    }
    .stRadio > div { gap: 0.5rem; }
    .proof-badge {
        background: #1e3a2a;
        border-left: 4px solid #00843D;
        padding: 0.5rem 0.75rem;
        border-radius: 4px;
        font-size: 0.95rem;
        margin-top: 0.4rem;
    }
    .source-banner {
        background: #1a1f2e;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        font-size: 0.9rem;
        margin-bottom: 0.75rem;
    }
    .badge-assigned {
        background: #1e3a2a;
        color: #4ade80;
        border: 1px solid #00843D;
        border-radius: 12px;
        padding: 0.15rem 0.6rem;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .badge-own-notes {
        background: #2a2a2a;
        color: #9ca3af;
        border: 1px solid #4b5563;
        border-radius: 12px;
        padding: 0.15rem 0.6rem;
        font-size: 0.85rem;
        font-weight: 600;
    }
    mark {
        background-color: #fef08a;
        color: #1a1a1a;
        border-radius: 2px;
        padding: 0 2px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Load sample index ─────────────────────────────────────────────────────────
SAMPLES_DIR = pathlib.Path(__file__).parent.parent / "samples"
_index_path = SAMPLES_DIR / "samples_index.json"
_samples: list[dict[str, Any]] = []
if _index_path.exists():
    with open(_index_path) as f:
        _samples = json.load(f)

# ── Header ────────────────────────────────────────────────────────────────────
st.title(f"📖 {config.PRODUCT_NAME}")
st.markdown(f"*{config.TAGLINE}*")
st.divider()

# ── Source picker ─────────────────────────────────────────────────────────────
st.markdown("### 1 · Choose your reading")

sample_labels = [f"{s['course']} — Week {s['week']}: {s['title']}" for s in _samples]
source_options = sample_labels + ["Paste / upload my own"]

# Fix #7: default to first sample reading (index 0), not "Paste / upload my own"
_default_index = 0 if sample_labels else len(source_options) - 1
source_choice = st.selectbox(
    "Reading source", source_options, index=_default_index, label_visibility="collapsed"
)

reading_text = ""       # raw file/pasted text (shown in source banner)
body_text = ""          # text after strip_metadata (fed to AI)
source_meta: dict[str, Any] = {}
is_assigned = False     # True when a sample from the assigned list is loaded

if source_choice == "Paste / upload my own":
    # ── "Your own notes" badge ────────────────────────────────────────────────
    st.markdown(
        "<span class='badge-own-notes'>📋 Your own notes — not checked against an assigned reading</span>",
        unsafe_allow_html=True,
    )

    # Upload widget (txt + pdf)
    uploaded = st.file_uploader("Upload a .txt or .pdf file (optional)", type=["txt", "pdf"])
    if uploaded is not None:
        if uploaded.name.endswith(".pdf"):
            try:
                import pypdf  # noqa: PLC0415

                reader = pypdf.PdfReader(uploaded)
                reading_text = "\n\n".join(
                    page_obj.extract_text() or "" for page_obj in reader.pages
                )
            except Exception as exc:
                st.warning(f"Could not read PDF: {exc}")
        else:
            reading_text = uploaded.read().decode("utf-8", errors="replace")

    pasted = st.text_area(
        "Or paste your reading here:",
        value=reading_text,
        height=180,
        placeholder="Paste your course reading here — at least a few sentences…",
    )
    reading_text = pasted
    body_text = reading_text  # pasted text has no metadata header to strip

else:
    # Find matching sample
    idx = source_options.index(source_choice)  # already 0-based into _samples
    source_meta = _samples[idx]
    is_assigned = True
    sample_path = SAMPLES_DIR / source_meta["file"]
    if sample_path.exists():
        reading_text = sample_path.read_text(encoding="utf-8")
        # Fix #1: strip header/metadata before passing to AI
        body_text = strip_metadata(reading_text)

    # ── Always-visible source banner ─────────────────────────────────────────
    st.markdown(
        f"<div class='source-banner'>"
        f"📚 Built only from your instructor's assigned reading &nbsp;·&nbsp; "
        f"<b>{source_meta['course']}</b> &nbsp;·&nbsp; "
        f"Week {source_meta['week']} &nbsp;·&nbsp; "
        f"<em>{source_meta['title']}</em> &nbsp;·&nbsp; "
        f"Assigned by {source_meta.get('assigned_by', '')}"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── "Instructor-assigned" badge ───────────────────────────────────────────
    st.markdown(
        "<span class='badge-assigned'>✅ Instructor-assigned</span>",
        unsafe_allow_html=True,
    )

    # ── Fingerprint check ─────────────────────────────────────────────────────
    expected_fp = source_meta.get("sha256", "")
    if expected_fp and body_text:
        fp_ok = fingerprint_check(body_text, expected_fp)
        short_fp = expected_fp[:8] + "…"
        if fp_ok:
            st.caption(f"🔒 Matches the file your instructor assigned (fingerprint {short_fp})")
        else:
            st.warning(
                "⚠️ This file's content does not match the fingerprint recorded when it was assigned. "
                "The reading may have been modified. Contact your instructor to confirm."
            )

    # Show reading in an expander so it doesn't dominate the screen
    with st.expander("Show full reading text"):
        st.text(reading_text)

# ── State management ──────────────────────────────────────────────────────────
if "passages" not in st.session_state:
    st.session_state["passages"] = {}
if "summary_result" not in st.session_state:
    st.session_state["summary_result"] = None
if "questions_result" not in st.session_state:
    st.session_state["questions_result"] = None
if "glossary_result" not in st.session_state:
    st.session_state["glossary_result"] = None
if "checked" not in st.session_state:
    st.session_state["checked"] = {}  # q_index -> bool (True = correct, False = wrong)
if "answers" not in st.session_state:
    st.session_state["answers"] = {}  # q_index -> chosen option index
if "night_sets" not in st.session_state:
    hour = __import__("datetime").datetime.now().hour
    st.session_state["night_sets"] = 1 if 21 <= hour or hour < 6 else 0

# ── Single "Make my study set" button (Fix #5) ────────────────────────────────
st.divider()
st.markdown("### 2 · Build your study set")

# ── F1: Reading-level and language controls ───────────────────────────────────
_lang_labels = [lbl for lbl, _ in config.SUPPORTED_LANGUAGES]
_lang_bcp47 = {lbl: code for lbl, code in config.SUPPORTED_LANGUAGES}

col_level, col_lang = st.columns(2)
with col_level:
    reading_level = st.radio(
        "Reading level",
        options=config.READING_LEVELS,
        index=0,
        horizontal=True,
        help="Simple: short sentences, everyday words (Grade 5–6). Standard: Grade 8–9.",
    )
with col_lang:
    language = st.selectbox(
        "Language",
        options=_lang_labels,
        index=0,
    )

show_english = False
if language != "English":
    show_english = st.toggle("Show English too", value=False)

can_build = len(body_text.strip()) >= 50
do_build = st.button(
    "📚 Make my study set",
    disabled=not can_build,
    type="primary",
)
if not can_build:
    st.caption("Paste or upload a reading first (at least a sentence or two).")

if do_build:
    passages = split_passages(body_text)
    st.session_state["passages"] = passages
    st.session_state["checked"] = {}
    st.session_state["answers"] = {}
    st.session_state["reading_level"] = reading_level
    st.session_state["language"] = language
    hour = __import__("datetime").datetime.now().hour
    if 21 <= hour or hour < 6:
        st.session_state["night_sets"] = st.session_state.get("night_sets", 0) + 1
    # Single spinner — all three AI calls run concurrently
    with st.spinner("Making your study set (about 15 seconds)…"):
        from concurrent.futures import ThreadPoolExecutor as _TPE

        with _TPE(max_workers=3) as _pool:
            _fs = _pool.submit(summarise, passages, ask, reading_level, language)
            _fq = _pool.submit(make_questions, passages, ask, reading_level, language)
            _fg = _pool.submit(make_glossary, passages, ask, language)
            sum_result = _fs.result()
            q_result = _fq.result()
            gloss_result = _fg.result()
    st.session_state["summary_result"] = sum_result
    st.session_state["questions_result"] = q_result
    st.session_state["glossary_result"] = gloss_result
    st.session_state["body_text_hash"] = body_text  # used for FK grade of original

# ── Summary display (Fix #2 + F1) ─────────────────────────────────────────────
summary_result = st.session_state.get("summary_result")
_stored_level = st.session_state.get("reading_level", "Simple")
_stored_lang = st.session_state.get("language", "English")

if summary_result:
    bullets = summary_result.get("bullets", [])
    dropped = summary_result.get("dropped", 0)
    backend = summary_result.get("backend", "offline")

    st.markdown("#### Summary")

    # ── F1: Flesch-Kincaid grade caption ─────────────────────────────────────
    _orig_text = st.session_state.get("body_text_hash", "")
    if _orig_text:
        _grade_before = flesch_kincaid_grade(_orig_text)
        # Collect English summary text for FK after
        _summary_en_text = " ".join(
            b.get("text_en") or b.get("text", "") for b in bullets
        )
        _grade_after = flesch_kincaid_grade(_summary_en_text) if _summary_en_text else 0.0
        if _grade_before > 0 and _grade_after > 0:
            st.caption(
                f"📊 Reading level: Grade {_grade_before} (original) → Grade {_grade_after} (your summary)"
            )

    # ── Bullets ───────────────────────────────────────────────────────────────
    for b in bullets:
        pid = b.get("passage_id", "")
        st.markdown(f"• {b['text']}  `[{pid}]`")
        # F1: Show English too (when non-English and toggle is on)
        if show_english and _stored_lang != "English":
            en_text = b.get("text_en", "")
            if en_text and en_text != b["text"]:
                st.caption(f"🇬🇧 {en_text}")
        # Proof in a small expander
        proof = b.get("proof") or b.get("proof_text", "")
        if proof:
            with st.expander("Where is this in my reading?"):
                st.markdown(f"> {proof}")

    if dropped:
        st.caption(f"ℹ️ {dropped} AI item(s) could not be verified against your reading and were removed.")

    # ── F1: Read aloud button ─────────────────────────────────────────────────
    if bullets:
        _aloud_text = " ".join(b.get("text", "") for b in bullets)
        _bcp47 = _lang_bcp47.get(_stored_lang, "en-US")
        _safe_text = _aloud_text.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
        if st.button("🔊 Read aloud", key="read_aloud_btn"):
            components.html(
                f"""<script>
                (function(){{
                    if (!window.speechSynthesis) return;
                    window.speechSynthesis.cancel();
                    var u = new SpeechSynthesisUtterance(`{_safe_text}`);
                    u.lang = "{_bcp47}";
                    u.rate = 0.85;
                    window.speechSynthesis.speak(u);
                }})();
                </script>""",
                height=0,
            )

    # ── F1: Offline language notice ───────────────────────────────────────────
    if backend == "offline" and _stored_lang != "English":
        st.info(
            "ℹ️ **Offline mode** — language and reading-level preferences are noted but "
            "the AI is not available right now, so the summary is in English. "
            "Connect to an AI backend to get your summary in the chosen language."
        )

    # ── F1: Glossary expander ─────────────────────────────────────────────────
    glossary_result = st.session_state.get("glossary_result")
    if glossary_result:
        terms = glossary_result.get("terms", [])
        if terms:
            with st.expander("📚 5 key words, explained simply"):
                for t in terms:
                    term_display = t.get("term", t.get("term_en", ""))
                    term_en = t.get("term_en", "")
                    defn = t.get("definition", "")
                    if _stored_lang != "English" and term_en and term_en != term_display:
                        st.markdown(f"**{term_display}** *(EN: {term_en})* — {defn}")
                    else:
                        st.markdown(f"**{term_display}** — {defn}")

    st.caption(f"🤖 Powered by **{backend}** · AI can make mistakes — every answer is checked against your reading.")

# ── Practice questions display ────────────────────────────────────────────────
q_result = st.session_state.get("questions_result")
if q_result:
    questions = q_result.get("questions", [])
    q_dropped = q_result.get("dropped", 0)
    q_backend = q_result.get("backend", "offline")

    st.divider()
    st.markdown("### 3 · Practice questions")

    # ── F2: Proof counter ─────────────────────────────────────────────────────
    total_q = len(questions)
    q_with_proof = sum(1 for q in questions if q.get("proof_text", "").strip())
    if q_dropped:
        st.info(
            f"✅ **{q_with_proof} of {total_q} questions checked against your reading** "
            f"(+ {q_dropped} removed because they could not be verified)"
        )
    else:
        st.info(f"✅ **{q_with_proof} of {total_q} questions checked against your reading**")

    passages = st.session_state.get("passages", {})

    for i, q in enumerate(questions):
        st.markdown(f"**Q{i + 1}. {q['stem']}**  `[{q.get('passage_id', '')}]`")
        # F1: Show English stem when non-English and toggle is on
        if show_english and _stored_lang != "English":
            stem_en = q.get("stem_en", "")
            if stem_en and stem_en != q["stem"]:
                st.caption(f"🇬🇧 {stem_en}")
        opts = q.get("options", [])
        radio_key = f"radio_{i}"

        chosen = st.radio(
            f"Options for Q{i + 1}",
            options=list(range(len(opts))),
            format_func=lambda x, o=opts: o[x],  # noqa: B023
            key=radio_key,
            index=st.session_state["answers"].get(i, 0),
            label_visibility="collapsed",
        )
        st.session_state["answers"][i] = chosen

        check_key = f"check_{i}"
        if st.button("✅ Check answer", key=check_key):
            is_correct = chosen == q.get("correct_index", 0)
            st.session_state["checked"][i] = is_correct

        if i in st.session_state["checked"]:
            is_correct = st.session_state["checked"][i]
            if is_correct:
                st.success("Correct! ✓")
            else:
                correct_opt = opts[q["correct_index"]] if opts else ""
                st.error(f"Not quite. The correct answer is: **{correct_opt}**")

            # F2: show EXACT proof sentence always (not only on wrong answers)
            pid = q.get("passage_id", "")
            proof = q.get("proof_text", "")
            if proof:
                proof_html = (
                    f"<div class='proof-badge'>"
                    f"\U0001f50d <b>Found in your reading</b> <code>[{pid}]</code><br>"
                    f"<em>\u201c{proof}\u201d</em>"
                    f"</div>"
                )
                st.markdown(proof_html, unsafe_allow_html=True)

                # F2: "Show me in the reading" expander with highlighted proof sentence
                full_passage = passages.get(pid, "")
                if full_passage:
                    with st.expander("📖 Show me in the reading"):
                        highlighted_html = highlight_proof(full_passage, proof)
                        st.markdown(highlighted_html, unsafe_allow_html=True)

        st.markdown("---")

    # ── Stats row (Fix #4: recompute on every render, stats always current) ───
    st.divider()
    st.markdown("### Tonight's stats")
    # Fix #4: read from checked state which is updated on every Check press
    total_answered = len(st.session_state["checked"])
    total_correct = sum(1 for v in st.session_state["checked"].values() if v)
    c1, c2, c3 = st.columns(3)
    c1.metric("Score", f"{total_correct} / {total_answered}" if total_answered else "—")
    accuracy = round(total_correct / total_answered * 100) if total_answered else 0
    c2.metric("Accuracy", f"{accuracy} %" if total_answered else "—")
    c3.metric("🌙 Late-night sets", st.session_state.get("night_sets", 0))

    st.caption(
        f"🤖 Questions powered by **{q_backend}** · "
        "AI can make mistakes — every answer is checked against your reading."
    )

    # ── Ask a person placeholder ──────────────────────────────────────────────
    st.divider()
    with st.expander("💬 Ask a person — get help from a human tutor"):
        st.info(
            "In the full version a prefilled form would open here (course, week, your question). "
            "A tutor would respond by the next business day. "
            "**No data is stored in this Phase 2 prototype.**"
        )
        course_name = source_meta.get("course", source_choice) if source_meta else source_choice
        week_no = source_meta.get("week", "—") if source_meta else "—"
        st.text_input("Course", value=course_name, disabled=True)
        st.text_input("Week", value=str(week_no), disabled=True)
        question_txt = st.text_area("Your question (demo only — not sent anywhere):", height=80)
        if st.button("Send (demo — no data stored)"):
            st.success("Your question has been noted. A tutor will respond by the next business day.")

    st.caption(
        "Ivy Tech IT Challenge 2026 · "
        f"{config.PRODUCT_NAME} · "
        f"{config.PILLAR} · "
        f"{config.STRATEGY}"
    )
