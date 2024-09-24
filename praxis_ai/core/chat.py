# core/chat.py

import ell
from ..config.settings import CHAT_MODEL, PRAXIS_NAME
from ..workspace_manager import WorkspaceManager
from typing import List

workspace_manager = WorkspaceManager()

@ell.complex(model=CHAT_MODEL)
def chat(user_input: str, conversation_history: List[str], workspace_name: str):
    """Praxis AI Chat function that handles user interactions."""
    workspace_path = workspace_manager.get_workspace_path(workspace_name)

    system_message = (
        f"You are {PRAXIS_NAME}, an AI assistant. You are currently in the '{workspace_name}' workspace "
        f"located at {workspace_path}. Your role is to assist the user with their queries and tasks, "
        f"considering the context of the current workspace and the conversation history. "
        f"Always provide helpful, accurate, and context-aware responses."
    )

    messages = [
        ell.system(system_message),
        *[ell.user(message) if i % 2 == 0 else ell.assistant(message) for i, message in enumerate(conversation_history)],
        ell.user(user_input)
    ]

    return messages