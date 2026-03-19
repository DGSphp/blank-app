from typing import Any

import pandas as pd


def compute_summary_stats(df: pd.DataFrame, column: str) -> dict[str, Any]:
    """Compute basic summary statistics for a numeric column."""
    series = df[column]
    return {
        "count": int(series.count()),
        "mean": float(series.mean()),
        "median": float(series.median()),
        "std": float(series.std()),
        "min": float(series.min()),
        "max": float(series.max()),
    }


def filter_dataframe(
    df: pd.DataFrame, column: str, values: list[str]
) -> pd.DataFrame:
    """Return rows where `column` matches any of the given values."""
    if not values:
        return df.iloc[0:0]
    return df[df[column].isin(values)]
