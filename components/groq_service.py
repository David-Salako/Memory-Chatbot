import os
from pathlib import Path
from typing import Any

import streamlit as st

from config import MAX_TOKENS

try:
    from groq import Groq
except ImportError:  # pragma: no cover - handled for Streamlit deployment
    Groq = Any  # type: ignore[misc]

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"


def _load_env_file() -> None:
    if not ENV_FILE.exists():
        return

    content = ENV_FILE.read_text(encoding="utf-8-sig")
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and value:
            os.environ.setdefault(key, value)


_load_env_file()


def get_api_key() -> str | None:
    """Check Streamlit secrets first, then fall back to environment variables."""
    try:
        if "GROQ_API_KEY" in st.secrets:
            value = st.secrets["GROQ_API_KEY"]
            if value:
                return str(value).strip()
    except Exception:
        pass

    value = os.environ.get("GROQ_API_KEY")
    if value:
        return str(value).strip()
    return None


@st.cache_resource(show_spinner=False)
def get_client(api_key: str) -> Any:
    if "Groq" not in globals() or getattr(globals()["Groq"], "__module__", "") != "groq":
        raise RuntimeError("The 'groq' package is not installed. Install it to use the chatbot.")
    return Groq(api_key=api_key)


def call_groq(client: Any, messages: list[dict], model: str, temperature: float) -> str:
    """Send the full message history to Groq and return the assistant's reply text."""
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=MAX_TOKENS,
    )
    return response.choices[0].message.content