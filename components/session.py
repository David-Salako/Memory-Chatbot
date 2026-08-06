"""
Streamlit session state setup.

Everything the app needs to remember for the life of the browser tab
lives in st.session_state. This module is the single place that
initializes it, so it's obvious what state exists.
"""

import streamlit as st

from config import DEFAULT_MODEL, DEFAULT_TEMPERATURE


def init_session_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "model" not in st.session_state:
        st.session_state.model = DEFAULT_MODEL
    if "temperature" not in st.session_state:
        st.session_state.temperature = DEFAULT_TEMPERATURE
    if "pruned_count" not in st.session_state:
        st.session_state.pruned_count = 0


def clear_chat() -> None:
    st.session_state.messages = []
    st.session_state.pruned_count = 0
