"""
Groq API integration.

Handles locating the API key, creating a cached client, and sending the
chat completion request.
"""

import os
import tomllib
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

from config import MAX_TOKENS

load_dotenv()  # reads .env into os.environ for local development
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def get_api_key() -> str | None:
    """Check session state, Streamlit secrets, environment variables, and local config files."""
    for key_name in ("groq_api_key", "groq_api_key_input", "GROQ_API_KEY"):
        try:
            value = st.session_state.get(key_name)
            if value:
                return str(value).strip()
        except Exception:
            pass

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

    secrets_path = PROJECT_ROOT / ".streamlit" / "secrets.toml"
    if secrets_path.exists():
        try:
            with secrets_path.open("rb") as fh:
                data = tomllib.load(fh)
            value = data.get("GROQ_API_KEY")
            if value:
                return str(value).strip()
        except Exception:
            pass

    return None


@st.cache_resource(show_spinner=False)
def get_client(api_key: str) -> Groq:
    return Groq(api_key=api_key)


def call_groq(client: Groq, messages: list[dict], model: str, temperature: float) -> str:
    """Send the full message history to Groq and return the assistant's reply text."""
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=MAX_TOKENS,
    )
    return response.choices[0].message.content