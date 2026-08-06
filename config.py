"""
Central configuration for the Groq Memory Chatbot.
Keeping constants here means nothing important is buried inside app.py.
"""

# Sliding window: max number of (user, assistant) message pairs kept in memory
MAX_MESSAGE_PAIRS = 20

# Where saved conversations get written to disk
HISTORY_FILE = "chat_history.json"

# Models available in the sidebar dropdown
AVAILABLE_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]

DEFAULT_MODEL = AVAILABLE_MODELS[0]
DEFAULT_TEMPERATURE = 0.7
MAX_INPUT_CHARS = 8000
MAX_TOKENS = 1024

PAGE_TITLE = "Groq Memory Chatbot"
PAGE_ICON = "🧠"