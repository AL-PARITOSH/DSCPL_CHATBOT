
# memory_utils.py

from langchain_core.chat_history import InMemoryChatMessageHistory

# Store chat memory per session
user_histories = {}

def get_session_history(session_id: str = "default"):
    if session_id not in user_histories:
        user_histories[session_id] = InMemoryChatMessageHistory()
    return user_histories[session_id]
