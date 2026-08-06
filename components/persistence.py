"""
Simple file-based persistence for chat history (bonus feature).

Session memory disappears when the Streamlit server restarts, so this
gives users a way to save a snapshot to disk and reload it later.
"""

import json
from datetime import datetime

from config import HISTORY_FILE


def save_history_to_file(messages: list[dict], path: str = HISTORY_FILE) -> None:
    payload = {
        "saved_at": datetime.now().isoformat(timespec="seconds"),
        "messages": messages,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def load_history_from_file(path: str = HISTORY_FILE) -> list[dict]:
    import os

    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("messages", [])
