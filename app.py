import streamlit as st

from config import PAGE_TITLE
from components.session import init_session_state
from components.groq_service import get_api_key, get_client
from components.sidebar import render_sidebar
from components.chat_ui import render_message_history, handle_user_turn

# --- Page setup ---
st.set_page_config(page_title=PAGE_TITLE, layout="centered")
init_session_state()

# --- Sidebar (model/temperature controls, context indicator, chat management) ---
render_sidebar()

# --- Header ---
st.title(f"Memory Chatbot ")
st.caption("A stateful chat terminal that remembers your conversation during this session.")

# --- API key / client setup ---
api_key = get_api_key()

if not api_key:
    st.error(
        "No Groq API key found. Set `GROQ_API_KEY` as an environment variable, "
        "or add it to `.streamlit/secrets.toml` as:\n\n"
        "```toml\nGROQ_API_KEY = \"your-key-here\"\n```"
    )
    st.stop()

try:
    client = get_client(api_key)
except Exception as e:
    st.error(f"Failed to initialize Groq client: {e}")
    st.stop()

# --- Chat interface ---
render_message_history()

user_input = st.chat_input("Type your message...")
if user_input is not None:
    handle_user_turn(client, user_input)