"""Load, profile and clean whatever data the organisers hand out on the day."""

from __future__ import annotations

import io
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
SUPPORTED = (".csv", ".xlsx", ".xls", ".json", ".parquet", ".tsv")


def list_data_files() -> list[Path]:
    """All loadable files under data/, newest first (skips the sample folder last)."""
    files = [p for p in DATA_DIR.rglob("*") if p.suffix.lower() in SUPPORTED and p.is_file()]
    return sorted(files, key=lambda p: ("sample" in p.parts, -p.stat().st_mtime))


def read_any(source, name: str | None = None) -> pd.DataFrame:
    """Read a path or an uploaded file-like object by extension."""
    name = (name or getattr(source, "name", None) or str(source)).lower()
    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(source)
    if name.endswith(".json"):
        return pd.read_json(source)
    if name.endswith(".parquet"):
        return pd.read_parquet(source)
    if name.endswith(".tsv"):
        return pd.read_csv(source, sep="\t")
    if isinstance(source, (bytes, bytearray)):
        source = io.BytesIO(source)
    try:
        return pd.read_csv(source)
    except UnicodeDecodeError:
        if hasattr(source, "seek"):
            source.seek(0)
        return pd.read_csv(source, encoding="latin-1")


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Light, safe cleaning: tidy headers, trim strings, parse obvious dates/numbers."""
    df = df.copy()
    df.columns = [str(c).strip().replace("\n", " ") for c in df.columns]
    df = df.dropna(axis=1, how="all").dropna(axis=0, how="all")
    for col in df.columns:
        s = df[col]
        if s.dtype == object:
            s = s.astype("string").str.strip()
            as_num = pd.to_numeric(s.str.replace(r"[,$%]", "", regex=True), errors="coerce")
            if as_num.notna().mean() > 0.9 and s.notna().sum() > 0:
                df[col] = as_num
                continue
            lowered = col.lower()
            if any(k in lowered for k in ("date", "time", "term", "_at", "day")):
                as_dt = pd.to_datetime(s, errors="coerce")
                if as_dt.notna().mean() > 0.8:
                    df[col] = as_dt
                    continue
            df[col] = s
    return df


def profile(df: pd.DataFrame) -> pd.DataFrame:
    """One row per column: type, missingness, cardinality, example values."""
    rows = []
    for col in df.columns:
        s = df[col]
        rows.append(
            {
                "column": col,
                "dtype": str(s.dtype),
                "missing_%": round(100 * s.isna().mean(), 1),
                "unique": int(s.nunique(dropna=True)),
                "example": ", ".join(map(str, s.dropna().unique()[:3])),
            }
        )
    return pd.DataFrame(rows)


def column_kinds(df: pd.DataFrame) -> dict[str, list[str]]:
    numeric = df.select_dtypes(include=np.number).columns.tolist()
    dates = df.select_dtypes(include=["datetime", "datetimetz"]).columns.tolist()
    cats = [c for c in df.columns if c not in numeric + dates and df[c].nunique(dropna=True) <= 50]
    text = [c for c in df.columns if c not in numeric + dates + cats]
    return {"numeric": numeric, "date": dates, "categorical": cats, "text": text}


def describe_for_llm(df: pd.DataFrame, max_cols: int = 40) -> str:
    """Compact, token-cheap description of a dataframe for an LLM prompt."""
    kinds = column_kinds(df)
    lines = [f"Rows: {len(df):,}. Columns: {df.shape[1]}."]
    for col in df.columns[:max_cols]:
        s = df[col]
        if col in kinds["numeric"]:
            lines.append(
                f"- {col} (numeric): mean={s.mean():.3g}, min={s.min():.3g}, max={s.max():.3g}, "
                f"missing={s.isna().mean():.0%}"
            )
        elif col in kinds["categorical"]:
            top = s.value_counts(normalize=True).head(5)
            lines.append(f"- {col} (category): " + ", ".join(f"{k}={v:.0%}" for k, v in top.items()))
        else:
            lines.append(f"- {col} ({s.dtype}): e.g. {', '.join(map(str, s.dropna().unique()[:3]))}")
    return "\n".join(lines)


def demo_data(n: int = 1200, seed: int = 7) -> pd.DataFrame:
    """Synthetic placeholder ONLY for smoke-testing the shell before real data arrives."""
    rng = np.random.default_rng(seed)
    campus = rng.choice(["North", "South", "East", "West", "Central"], n)
    status = rng.choice(["Full-time", "Part-time"], n, p=[0.35, 0.65])
    age = rng.integers(17, 55, n)
    credits = rng.integers(3, 16, n)
    gpa = np.clip(rng.normal(2.8, 0.7, n), 0, 4).round(2)
    logins = rng.poisson(12, n)
    works = rng.choice([0, 1], n, p=[0.4, 0.6])
    z = -1.2 + 1.1 * (gpa - 2.8) + 0.05 * (logins - 12) - 0.4 * works + 0.3 * (status == "Full-time")
    outcome = (rng.random(n) < 1 / (1 + np.exp(-z))).astype(int)
    return pd.DataFrame(
        {
            "record_id": np.arange(1, n + 1),
            "campus": campus,
            "enrollment_status": status,
            "age": age,
            "credits_attempted": credits,
            "gpa": gpa,
            "lms_logins_30d": logins,
            "works_while_enrolled": works,
            "outcome": outcome,
        }
    )
