"""Shared page chrome.  Mobile-first (centered layout), no dataset picker."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from lib import config
from lib.data import clean, demo_data, read_any


def page(title: str, icon: str = "📖") -> None:
    st.set_page_config(
        page_title=f"{title} · {config.PRODUCT_NAME}",
        page_icon=icon,
        layout="centered",
    )
    with st.sidebar:
        st.markdown(f"### {config.PRODUCT_NAME}")
        st.caption(config.TAGLINE)
        st.markdown(f"**Pillar:** {config.PILLAR}")
        st.markdown(f"**Strategy:** {config.STRATEGY}")


# Keep get_df / _load_upload for Impact page and tests that need a dataframe.
@st.cache_data(show_spinner="Loading data…")
def _load_upload(raw: bytes, name: str) -> pd.DataFrame:
    return clean(read_any(raw, name=name))


def get_df() -> pd.DataFrame:
    return st.session_state.get("df", demo_data())
