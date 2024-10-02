import ell
from ..config.settings import CHAT_MODEL, PRAXIS_NAME, ENABLE_CALENDAR, REASONING
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
from .orchestrator import orchestrator
from .refiner import refiner
from .sub_agent import sub_agent
from ..config.models import AgentContext, Task

import uuid # import uuid
from rich.console import Console # import rich
from rich.panel import Panel # import rich

workspace_manager = WorkspaceManager()
console = Console() # initialize console

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
    - Reasoning mode: {"Enabled" if REASONING else "Disabled"}

    Your primary responsibilities:
    1. Assist users with queries and tasks, always considering the current workspace context and conversation history.
    2. Manage workspaces efficiently, including creation, navigation, and deletion.
    3. Execute file operations and project structuring within workspaces.
    4. Create, read, copy, move, and delete various file types including PDFs, Word documents, and Markdown files.
    5. Maintain and utilize conversation history for context-aware interactions.
    6. Perform web searches to gather information and answer user queries.
    7. Schedule meetings and manage calendar events using Google Calendar (if enabled).
    8. If reasoning mode is enabled, use the orchestrator, sub-agent, and refiner to break down complex tasks and provide detailed, step-by-step solutions.

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
    12. In reasoning mode, leverage the orchestrator, sub-agent, and refiner to provide comprehensive and well-reasoned responses.
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

    def is_complex_task(user_input: str) -> bool: # new function
        """Determine if a task is complex enough to warrant reasoning mode."""
        simple_tasks = [
            "enter workspace",
            "create workspace",
            "list workspaces",
            "delete workspace",
            "hello",
            "hi",
            "help"
        ]
        return not any(task in user_input.lower() for task in simple_tasks)

    if REASONING and is_complex_task(user_input): # updated condition
        console.print(Panel("Entering reasoning mode for complex task", style="bold green")) # rich print statement
        # Initialize the AgentContext
        context = AgentContext(objective=user_input, previous_results=[], tasks=[])

        while True:
            # Get the next sub-task from the orchestrator
            orchestrator_response = orchestrator(context)
            if orchestrator_response.text.startswith("The task is complete:"):
                # If the task is complete, use the refiner to generate the final output
                final_output = refiner(context)
                console.print(Panel(f"Refined output: {final_output.text}", style="bold blue")) # rich print statement
                return final_output

            # Create a new task for the sub-agent
            new_task = Task(
                id=str(uuid.uuid4()),  # Generate a unique ID for the task
                description=orchestrator_response.text,
                status="pending"  # Set an initial status for the task
            )
            context.tasks.append(new_task)

            # Execute the sub-task using the sub-agent
            sub_agent_response = sub_agent(new_task, context.tasks[:-1])
            new_task.result = sub_agent_response.text
            new_task.status = "completed"  # Update the status after execution

            # Update the context with the new result
            context.previous_results.append(new_task.result)
            console.print(Panel(f"Executing sub-task: {new_task.description}", style="yellow")) # rich print statement
            console.print(Panel(f"Sub-task result: {new_task.result}", style="green")) # rich print statement

    else:
        # If reasoning mode is disabled, use the standard chat completion
        console.print(Panel("Using standard chat mode", style="bold blue")) # rich print statement
        return messages