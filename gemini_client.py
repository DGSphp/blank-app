"""Google Gemini API client for fetching data."""

import google.generativeai as genai


def configure_gemini(api_key: str) -> None:
    """Configure the Gemini API with the provided key."""
    genai.configure(api_key=api_key)


def list_models() -> list[str]:
    """Return available Gemini model names."""
    models = genai.list_models()
    return [
        m.name
        for m in models
        if "generateContent" in (m.supported_generation_methods or [])
    ]


def generate_content(model_name: str, prompt: str) -> str:
    """Send a prompt to Gemini and return the response text."""
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text


def start_chat(model_name: str, history: list[dict] | None = None):
    """Start a chat session with the given model."""
    model = genai.GenerativeModel(model_name)
    return model.start_chat(history=history or [])


def chat_send(chat, message: str) -> str:
    """Send a message in an existing chat and return the response."""
    response = chat.send_message(message)
    return response.text
