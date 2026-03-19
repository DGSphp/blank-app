# CLAUDE.md

## Project Overview

This is a **Streamlit** web application — a blank starter template for building interactive Python web apps. It is licensed under Apache 2.0 and maintained by the Streamlit Community Cloud team.

## Repository Structure

```
.
├── streamlit_app.py        # Main application entry point
├── requirements.txt        # Python dependencies
├── .devcontainer/          # Dev container configuration (Python 3.11, Codespaces)
├── .github/CODEOWNERS      # Code ownership (@streamlit/community-cloud)
├── .gitignore              # Standard Python gitignore
├── LICENSE                 # Apache 2.0
└── README.md               # Project documentation
```

## Tech Stack

- **Language**: Python
- **Framework**: Streamlit
- **Python version**: 3.11 (per devcontainer config)

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

### Dev Container / Codespaces

The project includes a `.devcontainer/devcontainer.json` that automatically installs dependencies and starts the Streamlit server on attach. Port 8501 is forwarded with an auto-opening preview.

## Key Files

- **`streamlit_app.py`** — The single entry point. All app logic goes here (or in modules imported by it).
- **`requirements.txt`** — Add Python package dependencies here, one per line.

## Conventions

- Keep `streamlit_app.py` as the main entry point; Streamlit Community Cloud expects this filename.
- Add new dependencies to `requirements.txt`.
- Secrets should go in `.streamlit/secrets.toml` (gitignored, never commit).
- No test framework is currently configured; if adding tests, use `pytest`.

## Common Commands

| Task | Command |
|------|---------|
| Install deps | `pip install -r requirements.txt` |
| Run app | `streamlit run streamlit_app.py` |
| Run with CORS disabled (devcontainer) | `streamlit run streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false` |
