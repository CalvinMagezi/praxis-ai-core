# tools/conversation_history.py

import ell
from pathlib import Path
from ..workspace_manager import WorkspaceManager
from ..utils.logging import logger

workspace_manager = WorkspaceManager()

@ell.tool()
def update_conversation_history_tool(conversation: str, current_workspace: str) -> str:
    """Update the conversation history in a markdown file within the current workspace."""
    workspace_path = workspace_manager.get_workspace_path(current_workspace)
    if not workspace_path:
        return f"Error: No valid workspace path for workspace: {current_workspace}"

    history_file = Path(workspace_path) / "conversation_history.md"
    try:
        with open(history_file, 'a') as file:
            file.write(f"\n\n{conversation}")
        return f"Conversation history updated successfully in {history_file}"
    except Exception as e:
        error_message = f"Error updating conversation history: {history_file}. Error: {e}"
        logger.error(error_message)
        return error_message

@ell.tool()
def read_conversation_history_tool(current_workspace: str) -> str:
    """Read the conversation history from the markdown file in the current workspace."""
    workspace_path = workspace_manager.get_workspace_path(current_workspace)
    if not workspace_path:
        return f"Error: No valid workspace path for workspace: {current_workspace}"

    history_file = Path(workspace_path) / "conversation_history.md"
    try:
        with open(history_file, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        error_message = f"Error reading conversation history: {history_file}. Error: {e}"
        logger.error(error_message)
        return error_message