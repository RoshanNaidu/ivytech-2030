"""Consistent Plotly charts. One accent colour, neutral greys, readable defaults."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from lib.config import ACCENT

PALETTE = [ACCENT, "#2F6DB5", "#E07B39", "#7A5195", "#5BA3A0", "#C9A227", "#8C8C8C"]


def _style(fig: go.Figure, title: str | None = None) -> go.Figure:
    fig.update_layout(
        title=title,
        template="plotly_white",
        colorway=PALETTE,
        margin=dict(l=10, r=10, t=50 if title else 10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        font=dict(size=13),
    )
    return fig


def auto_chart(df: pd.DataFrame, x: str, y: str | None = None, color: str | None = None,
               agg: str = "mean") -> go.Figure:
    """Pick a sensible chart from the column types so nobody wastes time on chart choice."""
    xs = df[x]
    x_num = pd.api.types.is_numeric_dtype(xs) and xs.nunique() > 15
    x_date = pd.api.types.is_datetime64_any_dtype(xs)
    if y is None:
        if x_num:
            return _style(px.histogram(df, x=x, color=color, nbins=40), f"Distribution of {x}")
        counts = df.groupby([x] + ([color] if color else []), dropna=False).size().reset_index(name="count")
        return _style(px.bar(counts, x=x, y="count", color=color, barmode="group"), f"Count by {x}")
    y_num = pd.api.types.is_numeric_dtype(df[y])
    if x_date and y_num:
        g = df.groupby([pd.Grouper(key=x, freq="MS")] + ([color] if color else []))[y].agg(agg).reset_index()
        return _style(px.line(g, x=x, y=y, color=color, markers=True), f"{agg} of {y} over time")
    if x_num and y_num:
        return _style(px.scatter(df, x=x, y=y, color=color, opacity=0.6, trendline=None), f"{y} vs {x}")
    if y_num:
        g = df.groupby([x] + ([color] if color else []), dropna=False)[y].agg(agg).reset_index()
        return _style(px.bar(g, x=x, y=y, color=color, barmode="group"), f"{agg} of {y} by {x}")
    ct = pd.crosstab(df[x], df[y], normalize="index").reset_index().melt(id_vars=x, value_name="share")
    return _style(px.bar(ct, x=x, y="share", color=y, barmode="stack"), f"{y} mix by {x}")


def importance_bar(imp: pd.DataFrame, top: int = 12) -> go.Figure:
    d = imp.head(top).iloc[::-1]
    fig = px.bar(d, x="importance", y="feature", orientation="h", color_discrete_sequence=[ACCENT])
    return _style(fig, "What drives the outcome (permutation importance)")


def gauge(value: float, target: float, title: str, unit: str = "%") -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta", value=value, number={"suffix": unit},
        delta={"reference": target, "suffix": unit},
        gauge={"axis": {"range": [0, max(100, target * 1.2)]}, "bar": {"color": ACCENT},
               "threshold": {"line": {"color": "#E07B39", "width": 4}, "value": target}},
        title={"text": title},
    ))
    return _style(fig)


def trajectory(baseline: float, target: float, start_year: int = 2026, end_year: int = 2030,
               unit: str = "%") -> go.Figure:
    years = list(range(start_year, end_year + 1))
    step = (target - baseline) / (len(years) - 1)
    vals = [baseline + i * step for i in range(len(years))]
    fig = px.line(x=years, y=vals, markers=True, labels={"x": "Year", "y": unit},
                  color_discrete_sequence=[ACCENT])
    fig.add_hline(y=baseline, line_dash="dot", line_color="#8C8C8C", annotation_text="Today")
    return _style(fig, "Path to the 2030 target")
