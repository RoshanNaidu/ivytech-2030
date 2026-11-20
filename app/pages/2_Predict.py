import streamlit as st

from lib.charts import importance_bar
from lib.ml import train, usable_features
from lib.ui import get_df, page

page("Predict", "📈")
st.title("Predict & explain")
st.caption("A transparent baseline model: which factors drive the outcome, and who to reach first.")

df = get_df()
cols = df.columns.tolist()
default_target = next((c for c in cols if c.lower() in ("outcome", "target", "retained", "completed")), cols[-1])
target = st.selectbox("Outcome to predict", cols, index=cols.index(default_target))
feats = st.multiselect("Factors", [c for c in cols if c != target], default=usable_features(df, target))
kind = st.radio("Model", ["forest", "linear"], horizontal=True,
                format_func=lambda k: "Random forest (accuracy)" if k == "forest" else "Linear (simplest to explain)")

if not feats:
    st.info("Pick at least one factor.")
    st.stop()

with st.spinner("Training…"):
    res = train(df, target, feats, kind)

st.markdown(f"**{res.model_name}** on {len(df):,} rows, tested on a 25% hold-out.")
mcols = st.columns(len(res.metrics))
for col, (k, v) in zip(mcols, res.metrics.items(), strict=True):
    col.metric(k.replace("_", " "), f"{v:.3f}")
if res.task == "classification" and "baseline_accuracy" in res.metrics:
    lift = res.metrics["accuracy"] - res.metrics["baseline_accuracy"]
    st.caption(f"Accuracy lift over always guessing the most common outcome: {lift:+.1%}")

st.plotly_chart(importance_bar(res.importance), use_container_width=True)

if "probability" in res.scored:
    st.subheader("Highest-priority records (hold-out set)")
    positive = res.pipeline.classes_[1]
    low_first = st.toggle(f"Lowest probability of '{positive}' first (e.g. most at risk)", value=True)
    ranked = res.scored.sort_values("probability", ascending=low_first)
    st.dataframe(ranked.head(25), use_container_width=True)
    st.download_button("Download ranked list", ranked.to_csv(index=False), "priority_list.csv", "text/csv")
