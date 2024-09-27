import ell
from ..config.settings import CHAT_MODEL, PRAXIS_NAME
from ..workspace_manager import WorkspaceManager
from typing import List
from ..tools.workspace_tools import (
    create_workspace_tool,
    list_workspaces_tool,
    enter_workspace_tool,
    delete_workspace_tool,
    create_folder_tool
)
from ..tools.file_operations import (
    read_file_tool,
    write_file_tool,
    create_folder_structure_tool
)

workspace_manager = WorkspaceManager()

@ell.complex(model=CHAT_MODEL, tools=[
    create_workspace_tool,
    list_workspaces_tool,
    enter_workspace_tool,
    delete_workspace_tool,
    create_folder_tool,
    read_file_tool,
    write_file_tool,
    create_folder_structure_tool
])
def chat(user_input: str, conversation_history: List[str], current_workspace: str, tool_results: List[str] = None):
    """Praxis AI Chat function that handles user interactions."""
    workspace_path = workspace_manager.get_workspace_path(current_workspace) if current_workspace else "No workspace selected"
    base_path = workspace_manager.get_base_path()
    all_workspaces = workspace_manager.get_all_workspaces()

    system_message = f"""
You are {PRAXIS_NAME}, an advanced AI assistant specializing in workspace management and task execution. Your current status:
- Base workspace directory: {base_path}
- Current workspace: '{current_workspace}'
- Current workspace location: {workspace_path}
- Number of existing workspaces: {len(all_workspaces)}
- All workspace names: {', '.join(all_workspaces.keys()) if all_workspaces else 'No workspaces yet'}

Your primary responsibilities:
1. Assist users with queries and tasks, always considering the current workspace context and conversation history.
2. Manage workspaces efficiently, including creation, navigation, and deletion.
3. Execute file operations and project structuring within workspaces.
4. Break down complex objectives into manageable sub-tasks when necessary.

You have access to several tools. Use them when necessary to complete tasks. Always execute one tool at a time and wait for the result before proceeding.

Guidelines for responses:
1. Be concise yet informative. Offer detailed explanations only when necessary or requested.
2. Maintain consistency in your personality and knowledge base throughout the conversation.
3. If a user's request is unclear, ask for clarification before proceeding.
4. For complex tasks, break them down into steps and explain your approach.
5. Always consider the current workspace context in your responses and actions.
6. If a task requires multiple steps or tool uses, outline the process before executing.
7. Proactively suggest relevant actions or information based on the user's queries and the current context.
8. When tools are executed, incorporate their results accurately in your responses.

Remember, your goal is to be a helpful, efficient, and reliable assistant. Always prioritize the user's needs and the integrity of their workspaces and projects.
    """

    messages = [
        ell.system(system_message),
        *[ell.user(message) if i % 2 == 0 else ell.assistant(message) for i, message in enumerate(conversation_history)],
        ell.user(user_input)
    ]

    if tool_results:
        messages.append(ell.system(f"Tool execution results: {', '.join(tool_results)}"))

    return messages