import streamlit as st

from lib import config
from lib.ai import ask, provider
from lib.data import describe_for_llm
from lib.ui import get_df, page

page("Assistant", "💬")
st.title("Ask the data")
st.caption(f"AI backend: `{provider()}` (set `AI_PROVIDER` in `.env`)")

df = get_df()
SYSTEM = f"""You are an assistant inside {config.PRODUCT_NAME}, a prototype for Ivy Tech Community College.
Pillar: {config.PILLAR}. User persona: {config.PERSONA}. Problem: {config.PROBLEM}.
Answer in plain language for a college leader or student. Be concise, cite numbers from the data
summary when relevant, and say clearly when the data cannot answer a question.

Dataset summary:
{describe_for_llm(df)}"""

if "chat" not in st.session_state:
    st.session_state.chat = []

for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("e.g. Which group has the lowest outcome rate, and why might that be?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"), st.spinner("Thinking…"):
        ans = ask(prompt, SYSTEM, st.session_state.chat)
        st.markdown(ans.text)
        if ans.note:
            st.caption(ans.note)
    st.session_state.chat += [{"role": "user", "content": prompt}, {"role": "assistant", "content": ans.text}]

if st.session_state.chat and st.button("Clear conversation"):
    st.session_state.chat = []
    st.rerun()
