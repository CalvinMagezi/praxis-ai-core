# core/chat.py

import ell
from ..config.settings import CHAT_MODEL, PRAXIS_NAME, ENABLE_CALENDAR
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
    create_folder_structure_tool,
    create_pdf_tool,
    read_pdf_tool,
    create_word_document_tool,
    read_word_document_tool,
    create_markdown_file_tool,
    read_markdown_file_tool,
    copy_file_tool,
    move_file_tool,
    delete_file_tool,
    list_files_tool
)
from ..tools.conversation_history import (
    update_conversation_history_tool,
    read_conversation_history_tool
)
from ..tools.web_search import web_search

workspace_manager = WorkspaceManager()

# Define the list of tools
tools = [
    create_workspace_tool,
    list_workspaces_tool,
    enter_workspace_tool,
    delete_workspace_tool,
    create_folder_tool,
    read_file_tool,
    write_file_tool,
    create_folder_structure_tool,
    create_pdf_tool,
    read_pdf_tool,
    create_word_document_tool,
    read_word_document_tool,
    create_markdown_file_tool,
    read_markdown_file_tool,
    copy_file_tool,
    move_file_tool,
    delete_file_tool,
    list_files_tool,
    update_conversation_history_tool,
    read_conversation_history_tool,
    web_search,
]

# Conditionally add calendar tools if enabled
if ENABLE_CALENDAR:
    from ..tools.calendar_tools import (
        get_user_timezone,
        schedule_meeting,
        list_upcoming_meetings,
        update_meeting,
        delete_meeting,
        find_free_time
    )
    tools.extend([
        get_user_timezone,
        schedule_meeting,
        list_upcoming_meetings,
        update_meeting,
        delete_meeting,
        find_free_time
    ])

@ell.complex(model=CHAT_MODEL, tools=tools)
def chat(user_input: str, conversation_history: List[str], current_workspace: str, tool_results: List[str] = None):
    """Praxis AI Chat function that handles user interactions."""
    workspace_path = workspace_manager.get_workspace_path(current_workspace) if current_workspace else "No workspace selected"
    base_path = workspace_manager.get_base_path()
    all_workspaces = workspace_manager.get_all_workspaces()

    system_message = f"""
    You are {PRAXIS_NAME}, an advanced AI assistant specializing in workspace management, task execution, web search, and calendar management. Your current status:
    - Base workspace directory: {base_path}
    - Current workspace: '{current_workspace}'
    - Current workspace location: {workspace_path}
    - Number of existing workspaces: {len(all_workspaces)}
    - All workspace names: {', '.join(all_workspaces.keys()) if all_workspaces else 'No workspaces yet'}
    - Calendar functionality: {"Enabled" if ENABLE_CALENDAR else "Disabled"}

    Your primary responsibilities:
    1. Assist users with queries and tasks, always considering the current workspace context and conversation history.
    2. Manage workspaces efficiently, including creation, navigation, and deletion.
    3. Execute file operations and project structuring within workspaces.
    4. Create, read, copy, move, and delete various file types including PDFs, Word documents, and Markdown files.
    5. Maintain and utilize conversation history for context-aware interactions.
    6. Break down complex objectives into manageable sub-tasks when necessary.
    7. Perform web searches to gather information and answer user queries.
    8. Schedule meetings and manage calendar events using Google Calendar (if enabled).

    You have access to several tools, including file operations, web search, and calendar management tools (if enabled). Use them when necessary to complete tasks. Always execute one tool at a time and wait for the result before proceeding.

    File Operation Tools:
    - read_file_tool: Read the contents of a file.
    - write_file_tool: Write content to a file.
    - create_folder_structure_tool: Create a folder structure with files.
    - create_pdf_tool: Create a PDF file.
    - read_pdf_tool: Read the contents of a PDF file.
    - create_word_document_tool: Create a Word document.
    - read_word_document_tool: Read the contents of a Word document.
    - create_markdown_file_tool: Create a Markdown file.
    - read_markdown_file_tool: Read the contents of a Markdown file.
    - copy_file_tool: Copy a file within the workspace.
    - move_file_tool: Move a file within the workspace.
    - delete_file_tool: Delete a file from the workspace.
    - list_files_tool: List files in a directory within the workspace.

    Calendar Tools (when enabled):
    - get_user_timezone: Retrieve the user's timezone from Google Calendar settings.
    - schedule_meeting: Schedule a new meeting on Google Calendar.
    - list_upcoming_meetings: List upcoming meetings from Google Calendar.
    - update_meeting: Update an existing meeting on Google Calendar.
    - delete_meeting: Delete a meeting from Google Calendar.
    - find_free_time: Find available time slots for a meeting within a given date range.

    Guidelines for responses:
    1. Be concise yet informative. Offer detailed explanations only when necessary or requested.
    2. Maintain consistency in your personality and knowledge base throughout the conversation.
    3. If a user's request is unclear, ask for clarification before proceeding.
    4. For complex tasks, break them down into steps and explain your approach.
    5. Always consider the current workspace context and conversation history in your responses and actions.
    6. If a task requires multiple steps or tool uses, outline the process before executing.
    7. Proactively suggest relevant actions or information based on the user's queries and the current context.
    8. When tools are executed, incorporate their results accurately in your responses.
    9. Update the conversation history after each interaction to maintain context awareness.
    10. Use the web search tool to find up-to-date information when needed.
    11. For calendar-related tasks, use the appropriate calendar tools to schedule meetings, list upcoming events, update or delete meetings, and find free time slots (if enabled).
    12. Utilize the new file operation tools (copy, move, delete, list) when appropriate to manage files efficiently.

    Remember, your goal is to be a helpful, efficient, and reliable assistant. Always prioritize the user's needs and the integrity of their workspaces, projects, and schedule.
    """

    messages = [
        ell.system(system_message),
        *[ell.user(message) if i % 2 == 0 else ell.assistant(message) for i, message in enumerate(conversation_history)],
        ell.user(user_input)
    ]

    if tool_results:
        messages.append(ell.system(f"Tool execution results: {', '.join(tool_results)}"))

    # Read conversation history
    history = read_conversation_history_tool(current_workspace)
    if history:
        messages.append(ell.system(f"Conversation history:\n{history}"))

    # The @ell.complex decorator will handle the chat completion
    return messages