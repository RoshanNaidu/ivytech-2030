"""Quick, explainable baseline models: pick a target, get a model + drivers in seconds."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, r2_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


@dataclass
class ModelResult:
    task: str                     # "classification" | "regression"
    model_name: str
    metrics: dict[str, float]
    importance: pd.DataFrame      # feature, importance (permutation, on held-out data)
    pipeline: Pipeline
    features: list[str]
    scored: pd.DataFrame          # held-out rows with prediction / probability


def infer_task(y: pd.Series) -> str:
    if not pd.api.types.is_numeric_dtype(y) or pd.api.types.is_bool_dtype(y) or y.nunique() <= 10:
        return "classification"
    return "regression"


def _preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    num = X.select_dtypes(include=np.number).columns.tolist()
    cat = [c for c in X.columns if c not in num]
    return ColumnTransformer(
        [
            ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), num),
            (
                "cat",
                Pipeline(
                    [
                        ("imp", SimpleImputer(strategy="most_frequent")),
                        ("oh", OneHotEncoder(handle_unknown="ignore", min_frequency=10)),
                    ]
                ),
                cat,
            ),
        ]
    )


def usable_features(df: pd.DataFrame, target: str) -> list[str]:
    """Drop the target, IDs, free text and dates (too high-cardinality for a quick baseline)."""
    keep = []
    for c in df.columns:
        if c == target:
            continue
        s = df[c]
        if "id" in c.lower().split("_") or c.lower().endswith("id"):
            continue
        if str(s.dtype).startswith("datetime"):
            continue
        if not pd.api.types.is_numeric_dtype(s) and s.nunique() > 50:
            continue
        keep.append(c)
    return keep


def train(df: pd.DataFrame, target: str, features: list[str] | None = None,
          kind: str = "forest", seed: int = 42) -> ModelResult:
    data = df.dropna(subset=[target]).copy()
    features = features or usable_features(data, target)
    X, y = data[features], data[target]
    task = infer_task(y)
    if task == "classification":
        y = y.astype(str)
        est = (RandomForestClassifier(n_estimators=300, min_samples_leaf=5, random_state=seed, n_jobs=-1)
               if kind == "forest" else LogisticRegression(max_iter=2000))
        strat = y if y.value_counts().min() >= 2 else None
    else:
        est = (RandomForestRegressor(n_estimators=300, min_samples_leaf=5, random_state=seed, n_jobs=-1)
               if kind == "forest" else LinearRegression())
        strat = None
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=seed, stratify=strat)
    pipe = Pipeline([("prep", _preprocessor(X)), ("model", est)]).fit(X_tr, y_tr)

    pred = pipe.predict(X_te)
    scored = X_te.copy()
    scored["actual"] = y_te.values
    scored["predicted"] = pred
    if task == "classification":
        metrics = {"accuracy": accuracy_score(y_te, pred), "f1_macro": f1_score(y_te, pred, average="macro")}
        if y.nunique() == 2:
            proba = pipe.predict_proba(X_te)[:, 1]
            scored["probability"] = proba
            metrics["roc_auc"] = roc_auc_score((y_te == pipe.classes_[1]).astype(int), proba)
        baseline = y_te.value_counts(normalize=True).iloc[0]
        metrics["baseline_accuracy"] = baseline
    else:
        metrics = {"r2": r2_score(y_te, pred), "mae": mean_absolute_error(y_te, pred)}

    imp = permutation_importance(pipe, X_te, y_te, n_repeats=5, random_state=seed, n_jobs=-1)
    importance = (pd.DataFrame({"feature": features, "importance": imp.importances_mean})
                  .sort_values("importance", ascending=False).reset_index(drop=True))
    name = f"{'Random forest' if kind == 'forest' else 'Linear'} {task}"
    return ModelResult(task, name, {k: float(v) for k, v in metrics.items()}, importance, pipe, features, scored)
