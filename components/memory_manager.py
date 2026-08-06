"""
Sliding Window (FIFO) memory manager.

The Groq chat endpoint is stateless -- it has no memory of previous
calls. To hold a real conversation, the entire message history has to
be re-sent on every turn. Left unchecked that list grows forever and
eventually blows past the model's context limit.

This module keeps it bounded: once the history exceeds a max number of
(user, assistant) pairs, the OLDEST pairs are dropped from the front of
the list -- First In, First Out -- leaving a rolling window of the most
recent, most relevant context.
"""

import streamlit as st

from config import MAX_MESSAGE_PAIRS


def apply_sliding_window(messages: list[dict], max_pairs: int = MAX_MESSAGE_PAIRS) -> list[dict]:
    """Trim messages down to the most recent max_pairs (user, assistant) pairs."""
    max_entries = max_pairs * 2
    if len(messages) <= max_entries:
        return messages

    excess = len(messages) - max_entries
    if excess % 2 != 0:
        excess += 1

    st.session_state.pruned_count += excess // 2
    return messages[excess:]
