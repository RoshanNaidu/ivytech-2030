"""Shared page chrome and the dataset that every page works on."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from lib import config
from lib.data import DATA_DIR, clean, demo_data, list_data_files, read_any


def page(title: str, icon: str = "🎓") -> None:
    st.set_page_config(page_title=f"{title} · {config.PRODUCT_NAME}", page_icon=icon, layout="wide")
    with st.sidebar:
        st.markdown(f"### {config.PRODUCT_NAME}")
        st.caption(config.TAGLINE)
        st.markdown(f"**Pillar:** {config.PILLAR}  \n**For:** {config.PERSONA}")
        st.divider()
        _data_picker()


@st.cache_data(show_spinner="Loading data…")
def _load_path(path: str) -> pd.DataFrame:
    return clean(read_any(path))


@st.cache_data(show_spinner="Loading data…")
def _load_upload(raw: bytes, name: str) -> pd.DataFrame:
    return clean(read_any(raw, name=name))


def _data_picker() -> None:
    st.markdown("**Dataset**")
    demo = "Demo data (synthetic placeholder)"
    paths = {str(p.relative_to(DATA_DIR)): p for p in list_data_files()}
    options = [*paths, demo]
    choice = st.selectbox("Source", options, index=0, label_visibility="collapsed")
    up = st.file_uploader("…or upload", type=["csv", "xlsx", "xls", "json", "parquet", "tsv"])
    if up is not None:
        st.session_state["df"] = _load_upload(up.getvalue(), up.name)
        st.session_state["df_name"] = up.name
    elif choice in paths:
        st.session_state["df"] = _load_path(str(paths[choice]))
        st.session_state["df_name"] = paths[choice].name
    else:
        st.session_state["df"] = demo_data()
        st.session_state["df_name"] = "demo data"
    df = st.session_state["df"]
    st.caption(f"{st.session_state['df_name']} · {len(df):,} rows × {df.shape[1]} cols")


def get_df() -> pd.DataFrame:
    return st.session_state.get("df", demo_data())
