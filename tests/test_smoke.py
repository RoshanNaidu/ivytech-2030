"""Fast smoke tests: the shell must load, profile, chart, model and answer offline."""

import os

from lib import ai, charts, data, ml


def test_data_pipeline():
    df = data.clean(data.demo_data(300))
    prof = data.profile(df)
    assert len(prof) == df.shape[1]
    kinds = data.column_kinds(df)
    assert "gpa" in kinds["numeric"] and "campus" in kinds["categorical"]
    assert "Rows: 300" in data.describe_for_llm(df)


def test_charts_build():
    df = data.demo_data(200)
    for x, y in [("campus", None), ("gpa", None), ("campus", "gpa"), ("age", "gpa"), ("campus", "enrollment_status")]:
        assert charts.auto_chart(df, x, y) is not None
    assert charts.trajectory(50, 60) is not None


def test_model_trains_and_explains():
    df = data.demo_data(600)
    res = ml.train(df, "outcome", kind="linear")
    assert res.task == "classification"
    assert "record_id" not in res.features
    assert 0 <= res.metrics["roc_auc"] <= 1
    assert res.importance.iloc[0]["feature"] in res.features


def test_ai_offline_never_crashes():
    os.environ["AI_PROVIDER"] = "offline"
    ans = ai.ask("hello")
    assert ans.backend == "offline" and "Offline" in ans.text
