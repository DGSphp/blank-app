import pandas as pd

from utils.stats import compute_summary_stats, filter_dataframe


def _sample_df() -> pd.DataFrame:
    return pd.DataFrame({
        "category": ["A", "A", "B", "B", "C"],
        "value": [10.0, 20.0, 30.0, 40.0, 50.0],
    })


def test_compute_summary_stats():
    df = _sample_df()
    stats = compute_summary_stats(df, "value")
    assert stats["count"] == 5
    assert stats["mean"] == 30.0
    assert stats["median"] == 30.0
    assert stats["min"] == 10.0
    assert stats["max"] == 50.0


def test_filter_dataframe_single():
    df = _sample_df()
    result = filter_dataframe(df, "category", ["A"])
    assert len(result) == 2
    assert (result["category"] == "A").all()


def test_filter_dataframe_multiple():
    df = _sample_df()
    result = filter_dataframe(df, "category", ["A", "C"])
    assert len(result) == 3


def test_filter_dataframe_empty_values():
    df = _sample_df()
    result = filter_dataframe(df, "category", [])
    assert len(result) == 0


def test_filter_dataframe_no_match():
    df = _sample_df()
    result = filter_dataframe(df, "category", ["Z"])
    assert len(result) == 0
