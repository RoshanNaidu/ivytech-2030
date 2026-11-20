import plotly.express as px
import streamlit as st

from lib.charts import auto_chart
from lib.data import column_kinds, profile
from lib.ui import get_df, page

page("Explore", "🔎")
st.title("Explore the data")

df = get_df()
kinds = column_kinds(df)

with st.expander("Data profile", expanded=True):
    st.dataframe(profile(df), use_container_width=True, hide_index=True)

st.subheader("Filter")
filtered = df
fcols = st.columns(3)
for i, col in enumerate(kinds["categorical"][:6]):
    vals = sorted(df[col].dropna().astype(str).unique())
    pick = fcols[i % 3].multiselect(col, vals)
    if pick:
        filtered = filtered[filtered[col].astype(str).isin(pick)]
st.caption(f"{len(filtered):,} of {len(df):,} rows")

st.subheader("Chart builder")
cols = df.columns.tolist()
a, b, c, d = st.columns(4)
x = a.selectbox("X", cols, index=cols.index(kinds["categorical"][0]) if kinds["categorical"] else 0)
y = b.selectbox("Y (optional)", [None, *cols], index=0)
color = c.selectbox("Colour by", [None, *kinds["categorical"]], index=0)
agg = d.selectbox("Aggregate", ["mean", "sum", "median", "count"], index=0)
if len(filtered):
    st.plotly_chart(auto_chart(filtered, x, y, color, agg), use_container_width=True)

if len(kinds["numeric"]) >= 2:
    with st.expander("Correlations between numeric fields"):
        corr = filtered[kinds["numeric"]].corr().round(2)
        st.plotly_chart(px.imshow(corr, text_auto=True, color_continuous_scale="RdBu", zmin=-1, zmax=1),
                        use_container_width=True)

st.download_button("Download filtered rows (CSV)", filtered.to_csv(index=False), "filtered.csv", "text/csv")
