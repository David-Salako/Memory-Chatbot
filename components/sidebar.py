"""
Sidebar UI: model/temperature controls, context window indicator,
and chat management buttons (clear / save / load).
"""

import streamlit as st

from config import AVAILABLE_MODELS, MAX_MESSAGE_PAIRS
from components.session import clear_chat
from components.persistence import save_history_to_file, load_history_from_file


def render_sidebar() -> None:
    with st.sidebar:
        st.header("⚙️ Settings")

        st.session_state.model = st.selectbox(
            "Model",
            AVAILABLE_MODELS,
            index=AVAILABLE_MODELS.index(st.session_state.model),
            help="Pick which Groq-hosted model handles the conversation.",
        )

        st.session_state.temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.5,
            value=st.session_state.temperature,
            step=0.05,
            help="Higher = more creative/random. Lower = more focused/deterministic.",
        )

        st.divider()
        _render_context_indicator()
        st.divider()
        _render_chat_controls()

        st.divider()
        st.caption("")


def _render_context_indicator() -> None:
    num_messages = len(st.session_state.messages)
    num_pairs = num_messages // 2
    usage_ratio = min(num_pairs / MAX_MESSAGE_PAIRS, 1.0)

    st.subheader("🧠 Context Window")
    st.progress(usage_ratio, text=f"{num_pairs}/{MAX_MESSAGE_PAIRS} pairs in memory")
    st.caption(f"Total messages in session: {num_messages}")

    if st.session_state.pruned_count > 0:
        st.caption(f"🧹 Pruned {st.session_state.pruned_count} old pair(s) via sliding window (FIFO).")


def _render_chat_controls() -> None:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗑️ Clear chat", use_container_width=True):
            clear_chat()
            st.rerun()

    with col2:
        if st.button("💾 Save chat", use_container_width=True):
            save_history_to_file(st.session_state.messages)
            st.success("Saved!")

    if st.button("📂 Load last saved chat", use_container_width=True):
        loaded = load_history_from_file()
        if loaded:
            st.session_state.messages = loaded
            st.success(f"Loaded {len(loaded)} messages.")
            st.rerun()
        else:
            st.info("No saved history found.")