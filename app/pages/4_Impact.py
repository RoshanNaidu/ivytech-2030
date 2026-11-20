import streamlit as st

from lib import config
from lib.charts import trajectory
from lib.ui import page

page("Impact", "🏆")
st.title("2030 impact")
st.caption("Turns the outcome target into numbers a college leader can act on.")

c1, c2, c3 = st.columns(3)
metric = c1.text_input("Metric", config.OUTCOME_METRIC)
baseline = c2.number_input("Baseline today", value=float(config.OUTCOME_BASELINE), step=0.5)
target = c3.number_input("2030 target", value=float(config.OUTCOME_TARGET), step=0.5)

c4, c5, c6 = st.columns(3)
population = c4.number_input("People affected statewide", value=config.STATEWIDE_HEADCOUNT, step=1000)
reach = c5.slider("Share reached by the tool", 0, 100, 40, format="%d%%") / 100
value_per = c6.number_input("Value per person improved ($, optional)", value=0, step=100)

delta_pts = target - baseline
people = population * reach * delta_pts / 100 if config.OUTCOME_UNIT == "%" else 0

m = st.columns(3)
m[0].metric(metric, f"{target:g}{config.OUTCOME_UNIT}", f"{delta_pts:+g} pts vs today")
m[1].metric("Additional people with the better outcome", f"{people:,.0f}")
m[2].metric("Estimated value", f"${people * value_per:,.0f}" if value_per else "n/a")

st.plotly_chart(trajectory(baseline, target, unit=config.OUTCOME_UNIT), use_container_width=True)

st.markdown(
    f"""
**Statewide rollout across {config.CAMPUSES} campuses** (edit in `docs/IMPACT_STATEMENT.md`):
pilot at one campus → measure against the baseline → expand by region → statewide by 2030.
"""
)
