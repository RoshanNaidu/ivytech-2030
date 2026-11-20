"""Landing page: who we serve, their problem, and the 2030 outcome we are moving."""

import streamlit as st

from lib import config
from lib.data import column_kinds
from lib.ui import get_df, page

page("Home")

st.title(config.PRODUCT_NAME)
st.subheader(config.TAGLINE)

c1, c2, c3 = st.columns(3)
c1.markdown(f"**Who we serve**  \n{config.PERSONA}")
c2.markdown(f"**Their problem**  \n{config.PROBLEM}")
c3.markdown(
    f"**2030 outcome**  \n{config.OUTCOME_METRIC}: "
    f"{config.OUTCOME_BASELINE:g}{config.OUTCOME_UNIT} → {config.OUTCOME_TARGET:g}{config.OUTCOME_UNIT}"
)

st.divider()
df = get_df()
kinds = column_kinds(df)
m = st.columns(4)
m[0].metric("Records", f"{len(df):,}")
m[1].metric("Columns", df.shape[1])
m[2].metric("Numeric fields", len(kinds["numeric"]))
m[3].metric("Category fields", len(kinds["categorical"]))

st.markdown(
    """
**How to use this prototype**
1. **Explore**: profile the data and find the pattern behind the problem.
2. **Predict**: see which factors drive the outcome and who is most at risk.
3. **Assistant**: ask questions about the data in plain English.
4. **Impact**: size the 2030 outcome and what a statewide rollout means.
"""
)
