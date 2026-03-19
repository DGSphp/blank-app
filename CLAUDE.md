# CLAUDE.md

## Project Overview

This is a **Streamlit** data explorer application that provides an interactive dashboard for visualizing and analyzing sample datasets. Built on the Streamlit blank app template, licensed under Apache 2.0.

## Repository Structure

```
.
├── streamlit_app.py        # Main application entry point (dashboard UI)
├── utils/                  # Reusable logic modules
│   ├── __init__.py
│   ├── data_generator.py   # Sample data generation with NumPy
│   ├── stats.py            # Summary statistics and filtering
│   └── charts.py           # Streamlit chart rendering functions
├── tests/                  # Pytest test suite
│   ├── __init__.py
│   ├── test_data_generator.py
│   └── test_stats.py
├── requirements.txt        # Python dependencies
├── .devcontainer/          # Dev container config (Python 3.11, Codespaces)
├── .github/CODEOWNERS      # Code ownership (@streamlit/community-cloud)
├── .gitignore              # Standard Python gitignore
├── LICENSE                 # Apache 2.0
└── README.md               # Project documentation
```

## Tech Stack

- **Language**: Python 3.11
- **Framework**: Streamlit
- **Data**: pandas, NumPy
- **Testing**: pytest

## Development Setup

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run streamlit_app.py
```

The app runs on port **8501** by default.

### Run tests

```bash
python -m pytest tests/ -v
```

### Dev Container / Codespaces

The `.devcontainer/devcontainer.json` auto-installs dependencies and starts the Streamlit server. Port 8501 is forwarded with auto-preview.

## Architecture

- **`streamlit_app.py`** — Dashboard entry point. Composes sidebar controls, metrics, and tabbed charts. Uses `@st.cache_data` for data caching.
- **`utils/data_generator.py`** — Generates reproducible sample DataFrames with dates, categories, values, and scores using `np.random.default_rng`.
- **`utils/stats.py`** — Pure functions for computing summary statistics and filtering DataFrames. No Streamlit dependency — easy to test.
- **`utils/charts.py`** — Thin wrappers around Streamlit chart functions. Handles empty-data edge cases.

## Conventions

- Keep `streamlit_app.py` as the main entry point; Streamlit Community Cloud expects this filename.
- Separate business logic (`utils/stats.py`, `utils/data_generator.py`) from UI code (`utils/charts.py`, `streamlit_app.py`) so logic is independently testable.
- Add new dependencies to `requirements.txt`.
- Secrets go in `.streamlit/secrets.toml` (gitignored, never commit).
- Tests use pytest. Keep test files in `tests/` mirroring the module they test.
- Use type hints on function signatures.

## Common Commands

| Task | Command |
|------|---------|
| Install deps | `pip install -r requirements.txt` |
| Run app | `streamlit run streamlit_app.py` |
| Run tests | `python -m pytest tests/ -v` |
| Run with CORS disabled (devcontainer) | `streamlit run streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false` |
