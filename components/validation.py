"""
Input Validation Gate.

Blocks empty / whitespace-only / oversized messages before they ever
reach the Groq API, preventing a 400 Bad Request from an empty payload.
"""

from config import MAX_INPUT_CHARS


def validate_input(text: str | None) -> tuple[bool, str]:
    """Return (is_valid, error_message)."""
    if text is None:
        return False, "No input received. Please type a message."

    if text.strip() == "":
        return False, "Message can't be empty or just whitespace. Type something first."

    if len(text) > MAX_INPUT_CHARS:
        return False, f"That message is too long (max {MAX_INPUT_CHARS} characters). Please shorten it."

    return True, ""
