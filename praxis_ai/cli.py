# cli.py

import os
import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich import print as rprint
from rich.markdown import Markdown
from dotenv import load_dotenv
from .core.chat import chat
from .workspace_manager import WorkspaceManager, WorkspaceError
from .config.models import AgentContext
from .utils.helpers import create_task
import inspect

# Import tools
from .tools.file_operations import (
    create_pdf_tool,
    read_pdf_tool,
    create_word_document_tool,
    read_word_document_tool,
    create_markdown_file_tool,
    read_markdown_file_tool
)
from .tools.conversation_history import (
    update_conversation_history_tool,
    read_conversation_history_tool
)
from .tools.web_search import web_search
from .tools.calendar_tools import schedule_meeting, list_upcoming_meetings

console = Console()
workspace_manager = WorkspaceManager()

def check_api_keys():
    load_dotenv()
    openai_key = os.getenv("OPENAI_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")
    google_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    if not openai_key:
        console.print("[yellow]No OpenAI API key found in environment variables.[/yellow]")
        openai_key = Prompt.ask("Please enter your OpenAI API key")
        os.environ["OPENAI_API_KEY"] = openai_key
        console.print("[green]OpenAI API key set successfully.[/green]")
    
    if not tavily_key:
        console.print("[yellow]No Tavily API key found in environment variables.[/yellow]")
        tavily_key = Prompt.ask("Please enter your Tavily API key")
        os.environ["TAVILY_API_KEY"] = tavily_key
        console.print("[green]Tavily API key set successfully.[/green]")
    
    if not google_credentials:
        console.print("[yellow]No Google Calendar credentials found in environment variables.[/yellow]")
        google_credentials = Prompt.ask("Please enter the path to your Google Calendar credentials file")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials
        console.print("[green]Google Calendar credentials set successfully.[/green]")
    
    return openai_key and tavily_key and google_credentials

def initialize_praxis():
    base_path = workspace_manager.get_base_path()
    workspaces = workspace_manager.get_all_workspaces()
    
    system_message = f"""
    Initialization complete. Praxis AI is now aware of the following:
    - Base workspace directory: {base_path}
    - Number of existing workspaces: {len(workspaces)}
    - Workspace names: {', '.join(workspaces.keys()) if workspaces else 'No workspaces yet'}
    
    Praxis is ready to assist with managing these workspaces, creating new ones as needed, and performing web searches for up-to-date information.
    """
    
    console.print(Panel(system_message, title="Praxis AI Initialization", border_style="green"))

@click.command()
def cli():
    """Praxis AI - Your intelligent workspace assistant with web search capabilities"""
    if not check_api_keys():
        console.print("[red]API keys are missing. Exiting.[/red]")
        return

    initialize_praxis()

    console.print(Panel.fit("Welcome to Praxis AI - Your intelligent workspace assistant with web search capabilities", border_style="cyan"))
    console.print("Type 'exit' to quit the chat at any time.")
    console.print("You can ask questions or request information, and Praxis will use its web search capability when needed.")

    conversation_history = []
    current_workspace = None
    tool_results = []

    while True:
        user_input = Prompt.ask("[bold cyan]You[/bold cyan]")

        if user_input.lower() == 'exit':
            break

        # Pass tool_results to the chat function
        response = chat(user_input, conversation_history, current_workspace, tool_results)

        # Handle the response, whether it's a string or a Message object
        assistant_response = response.text if hasattr(response, 'text') else str(response)

        console.print(Markdown(f"**Praxis**: {assistant_response}"))
        conversation_history.append(f"You: {user_input}")
        conversation_history.append(f"Praxis: {assistant_response}")

        # Update conversation history after each response
        update_conversation_history_tool(f"User: {user_input}\nPraxis: {assistant_response}", current_workspace)

        tool_results = []

        # Check if tool_calls exists and is not empty
        if hasattr(response, 'tool_calls') and response.tool_calls:
            for tool_call in response.tool_calls:
                tool_result = execute_tool(tool_call, current_workspace)
                tool_results.append(tool_result)

                # Update current workspace if it was changed during tool execution
                if "enter_workspace_tool" in str(tool_call):
                    current_workspace = tool_result.split("Entered workspace: ")[-1]

            # Get Praxis's response to the tool results
            response = chat(f"Tool execution results: {', '.join(tool_results)}", conversation_history, current_workspace, tool_results)
            assistant_response = response.text if hasattr(response, 'text') else str(response)

            console.print(Markdown(f"**Praxis**: {assistant_response}"))
            conversation_history.append(f"Praxis: {assistant_response}")

            # Update conversation history with tool results
            conversation_history.append(f"Praxis: {assistant_response}")
            update_conversation_history_tool(f"Tool Results: {', '.join(tool_results)}\nPraxis: {assistant_response}", current_workspace)

    console.print("[bold cyan]Thank you for using Praxis AI. Goodbye![/bold cyan]")

def execute_tool(tool_call, current_workspace):
    try:
        # Debug print to inspect the tool_call object
        rprint("[bold yellow]Debug: Tool Call Object:[/bold yellow]", tool_call)

        # Try to access different possible attributes
        if hasattr(tool_call, 'function'):  # Check for LangChain tools
            tool_name = getattr(tool_call.function, 'name', str(tool_call.function))
            tool_args = getattr(tool_call.function, 'arguments', {})
        elif hasattr(tool_call, 'tool'): # Check for other tool formats
            tool_name = getattr(tool_call.tool, '__name__', str(tool_call.tool))
            tool_args = tool_call.arguments if hasattr(tool_call, 'arguments') else {}
        else: # Fallback if tool structure is unknown
            tool_name = str(tool_call)
            tool_args = {}

        rprint(f"[bold cyan]Executing tool:[/bold cyan] {tool_name}")
        rprint(f"[bold cyan]Arguments:[/bold cyan] {tool_args}")

        # Add current_workspace to the arguments if it's expected by the tool
        if 'current_workspace' in inspect.signature(tool_call).parameters:
            tool_args['current_workspace'] = current_workspace

        # Execute the tool based on its structure
        if callable(tool_call):
            result = tool_call(**tool_args)
        elif hasattr(tool_call, 'tool') and callable(tool_call.tool):
            result = tool_call.tool(**tool_args)
        else:
            raise ValueError(f"Unable to execute tool: {tool_name}")

        # Handle rich formatting for web search results
        if tool_name == 'web_search':
            console.print(result)
            return "Web search results displayed."
        else:
            rprint(f"[bold green]Tool Execution Result:[/bold green] {result}")
            return result
    except Exception as e:
        error_message = f"Error executing tool: {str(e)}"
        console.print(f"[bold red]Error:[/bold red] {error_message}")
        return error_message

if __name__ == "__main__":
    cli()