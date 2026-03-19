# Gemini → Claude Data Transfer

A Streamlit webapp that transfers data from Google Gemini to Anthropic Claude. Send a prompt to Gemini, review the response, then transfer it to Claude for further analysis, refinement, or comparison.

## Features

- **Transfer Mode** — Query Gemini, then forward the response to Claude with custom instructions
- **Direct Compare** — Send the same prompt to both models side by side
- **History** — Review all past transfers in one place

## Getting Started

### Prerequisites

- Python 3.8+
- A [Google Gemini API key](https://aistudio.google.com/apikey)
- An [Anthropic Claude API key](https://console.anthropic.com/settings/keys)

### Installation

```bash
pip install -r requirements.txt
```

### Run

```bash
streamlit run streamlit_app.py
```

Enter your API keys in the sidebar and start transferring data.

## Project Structure

```
blank-app/
├── streamlit_app.py    # Main Streamlit UI
├── gemini_client.py    # Google Gemini API wrapper
├── claude_client.py    # Anthropic Claude API wrapper
├── requirements.txt    # Python dependencies
└── LICENSE             # Apache 2.0
```

## License

Apache License 2.0 — see [LICENSE](LICENSE).
