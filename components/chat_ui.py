import streamlit as st

from components.validation import validate_input
from components.memory_manager import apply_sliding_window
from components.groq_service import call_groq

try:
    from groq import APIError, APIConnectionError, RateLimitError, AuthenticationError
except ImportError:  # pragma: no cover - handled for Streamlit deployment
    class APIError(Exception):
        pass

    class APIConnectionError(Exception):
        pass

    class RateLimitError(Exception):
        pass

    class AuthenticationError(Exception):
        pass


def render_message_history() -> None:
    for msg in st.session_state.messages:
        avatar = "🧑" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])


def handle_user_turn(client, user_input: str) -> None:
    """Validate input, call the API, store the exchange, and prune history."""
    is_valid, error_msg = validate_input(user_input)

    if not is_valid:
        st.error(f"⚠️ {error_msg}")
        return

    # 1. Ingest & append the user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    # 2. Transmit the full history to Groq & record the response
    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        placeholder.markdown("Thinking...")
        try:
            reply = call_groq(
                client,
                st.session_state.messages,
                st.session_state.model,
                st.session_state.temperature,
            )
            placeholder.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

        except AuthenticationError:
            placeholder.error("❌ Invalid API key. Check your GROQ_API_KEY and try again.")

        except RateLimitError:
            placeholder.error("⏳ Rate limit or quota exceeded. Wait a moment and try again.")

        except APIConnectionError:
            placeholder.error("🌐 Connection error — couldn't reach Groq's API. Check your network.")

        except APIError as e:
            placeholder.error(f"🚨 Groq API error: {e}")

        except Exception as e:
            placeholder.error(f"Unexpected error: {e}")

    # 3. Apply sliding window (FIFO) pruning after the turn completes
    st.session_state.messages = apply_sliding_window(st.session_state.messages)
    st.rerun()