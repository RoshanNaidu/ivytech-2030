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

from lib import config
from lib.ai import ask
from lib.study import make_questions, split_passages, summarise
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

source_options = ["Paste / upload my own"] + [
    f"{s['course']} — Week {s['week']}: {s['title']}" for s in _samples
]
source_choice = st.selectbox("Reading source", source_options, label_visibility="collapsed")

reading_text = ""
source_meta: dict[str, Any] = {}

if source_choice == "Paste / upload my own":
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
else:
    # Find matching sample
    idx = source_options.index(source_choice) - 1  # offset by the "Paste" option
    source_meta = _samples[idx]
    sample_path = SAMPLES_DIR / source_meta["file"]
    if sample_path.exists():
        reading_text = sample_path.read_text(encoding="utf-8")
    # Show source banner
    st.markdown(
        f"<div class='source-banner'>"
        f"📚 <b>{source_meta['course']}</b> &nbsp;·&nbsp; "
        f"Week {source_meta['week']} &nbsp;·&nbsp; "
        f"<em>{source_meta['title']}</em> &nbsp;·&nbsp; "
        f"Assigned by {source_meta.get('assigned_by', '')}"
        f"</div>",
        unsafe_allow_html=True,
    )
    # Show reading in an expander so it doesn't dominate the screen
    with st.expander("Show full reading text"):
        st.text(reading_text)

# ── Summarise button ──────────────────────────────────────────────────────────
st.divider()
st.markdown("### 2 · Get a plain-language summary")

col_btn, col_note = st.columns([2, 3])
do_summarise = col_btn.button("📝 Summarise", disabled=len(reading_text.strip()) < 50)
if len(reading_text.strip()) < 50:
    col_note.caption("Paste or upload a reading first (at least a sentence or two).")

# ── State management ──────────────────────────────────────────────────────────
if "passages" not in st.session_state:
    st.session_state["passages"] = {}
if "summary_result" not in st.session_state:
    st.session_state["summary_result"] = None
if "questions_result" not in st.session_state:
    st.session_state["questions_result"] = None
if "checked" not in st.session_state:
    st.session_state["checked"] = {}  # q_index -> bool (True = correct, False = wrong)
if "answers" not in st.session_state:
    st.session_state["answers"] = {}  # q_index -> chosen option index
if "night_sets" not in st.session_state:
    hour = __import__("datetime").datetime.now().hour
    st.session_state["night_sets"] = 1 if 21 <= hour or hour < 6 else 0

if do_summarise:
    passages = split_passages(reading_text)
    st.session_state["passages"] = passages
    with st.spinner("Summarising…"):
        result = summarise(passages, ask)
    st.session_state["summary_result"] = result
    st.session_state["questions_result"] = None  # reset practice on new reading
    st.session_state["checked"] = {}
    st.session_state["answers"] = {}
    hour = __import__("datetime").datetime.now().hour
    if 21 <= hour or hour < 6:
        st.session_state["night_sets"] = st.session_state.get("night_sets", 0) + 1

# ── Summary display ───────────────────────────────────────────────────────────
summary_result = st.session_state.get("summary_result")
if summary_result:
    bullets = summary_result.get("bullets", [])
    dropped = summary_result.get("dropped", 0)
    backend = summary_result.get("backend", "offline")

    st.markdown("#### Summary")
    for b in bullets:
        pid = b.get("passage_id", "")
        st.markdown(f"• {b['text']}  `[{pid}]`")

    if dropped:
        st.caption(f"ℹ️ {dropped} AI item(s) could not be verified against your reading and were removed.")

    st.caption(f"🤖 Powered by **{backend}** · AI can make mistakes — every answer is checked against your reading.")

    # ── Practice button ───────────────────────────────────────────────────────
    st.divider()
    st.markdown("### 3 · Practice questions")
    if st.button("🎯 Generate practice questions"):
        passages = st.session_state["passages"]
        with st.spinner("Generating questions…"):
            q_result = make_questions(passages, ask)
        st.session_state["questions_result"] = q_result
        st.session_state["checked"] = {}
        st.session_state["answers"] = {}

# ── Practice questions display ────────────────────────────────────────────────
q_result = st.session_state.get("questions_result")
if q_result:
    questions = q_result.get("questions", [])
    q_dropped = q_result.get("dropped", 0)
    q_backend = q_result.get("backend", "offline")

    if q_dropped:
        st.caption(f"ℹ️ {q_dropped} AI question(s) could not be verified and were removed.")

    passages = st.session_state.get("passages", {})
    total_answered = len(st.session_state["checked"])
    total_correct = sum(1 for v in st.session_state["checked"].values() if v)

    for i, q in enumerate(questions):
        st.markdown(f"**Q{i + 1}. {q['stem']}**  `[{q.get('passage_id', '')}]`")
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

            # Always show proof
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

        st.markdown("---")

    # ── Stats row ─────────────────────────────────────────────────────────────
    st.divider()
    st.markdown("### Tonight's stats")
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
