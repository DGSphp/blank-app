from utils.data_generator import generate_sample_data


def test_generate_sample_data_default():
    df = generate_sample_data()
    assert len(df) == 200
    assert list(df.columns) == ["date", "category", "value", "score"]


def test_generate_sample_data_custom_rows():
    df = generate_sample_data(n_rows=50)
    assert len(df) == 50


def test_generate_sample_data_reproducible():
    df1 = generate_sample_data(seed=123)
    df2 = generate_sample_data(seed=123)
    assert df1.equals(df2)


def test_generate_sample_data_categories():
    df = generate_sample_data(n_rows=500, seed=0)
    assert set(df["category"].unique()).issubset({"A", "B", "C", "D"})


def test_generate_sample_data_score_range():
    df = generate_sample_data(n_rows=100, seed=7)
    assert (df["score"] >= 1).all()
    assert (df["score"] < 100).all()
