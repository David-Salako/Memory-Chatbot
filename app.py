import streamlit as st

from config import PAGE_TITLE
from components.session import init_session_state
from components.groq_service import get_api_key, get_client
from components.sidebar import render_sidebar
from components.chat_ui import render_message_history, handle_user_turn

try:
    import groq  # noqa: F401
except ImportError:
    groq = None

# --- Page setup ---
st.set_page_config(page_title=PAGE_TITLE, layout="centered")
init_session_state()

# --- Sidebar (model/temperature controls, context indicator, chat management) ---
render_sidebar()

# --- Header ---
st.title(f"Memory Chatbot ")
st.caption("A stateful chat terminal that remembers your conversation during this session.")

# --- API key / client setup ---
if groq is None:
    st.error("The 'groq' package is not available in this environment. Please ensure dependencies are installed before running the app.")
    st.stop()

api_key = get_api_key()

if not api_key:
    st.caption("No Groq API key was found. Enter one below for this session.")
    api_key = st.text_input("Groq API key", type="password", key="groq_api_key_input")
    if api_key:
        api_key = api_key.strip()
    else:
        st.error(
            "No Groq API key found. Enter it above, or configure it in Streamlit secrets as `GROQ_API_KEY`."
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