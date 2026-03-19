import numpy as np
import pandas as pd


def generate_sample_data(n_rows: int = 200, seed: int = 42) -> pd.DataFrame:
    """Generate a sample dataset with dates, categories, and numeric values."""
    rng = np.random.default_rng(seed)
    dates = pd.date_range(start="2024-01-01", periods=n_rows, freq="D")
    categories = rng.choice(["A", "B", "C", "D"], size=n_rows)
    values = rng.normal(loc=50, scale=15, size=n_rows).round(2)
    scores = rng.integers(low=1, high=100, size=n_rows)

    return pd.DataFrame({
        "date": dates,
        "category": categories,
        "value": values,
        "score": scores,
    })
