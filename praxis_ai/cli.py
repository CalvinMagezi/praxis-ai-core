# cli.py

import os
import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich import print as rprint
from dotenv import load_dotenv
from .core.chat import chat
from .workspace_manager import WorkspaceManager, WorkspaceError
from .config.models import AgentContext
from .utils.helpers import create_task
import inspect

# {{ edit_1: Import tools }}
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

console = Console()
workspace_manager = WorkspaceManager()

def check_api_key():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print("[yellow]No OpenAI API key found in environment variables.[/yellow]")
        api_key = Prompt.ask("Please enter your OpenAI API key")
        os.environ["OPENAI_API_KEY"] = api_key
        console.print("[green]API key set successfully.[/green]")
    return api_key

def initialize_praxis():
    base_path = workspace_manager.get_base_path()
    workspaces = workspace_manager.get_all_workspaces()
    
    system_message = f"""
    Initialization complete. Praxis AI is now aware of the following:
    - Base workspace directory: {base_path}
    - Number of existing workspaces: {len(workspaces)}
    - Workspace names: {', '.join(workspaces.keys()) if workspaces else 'No workspaces yet'}
    
    Praxis is ready to assist with managing these workspaces and creating new ones as needed.
    """
    
    console.print(Panel(system_message, title="Praxis AI Initialization", border_style="green"))

@click.command()
def cli():
    """Praxis AI - Your intelligent workspace assistant"""
    api_key = check_api_key()
    if not api_key:
        console.print("[red]No API key provided. Exiting.[/red]")
        return

    initialize_praxis()

    console.print(Panel.fit("Welcome to Praxis AI", border_style="cyan"))
    console.print("Type 'exit' to quit the chat at any time.")

    conversation_history = []
    current_workspace = None
    tool_results = []

    while True:
        user_input = Prompt.ask("[bold cyan]You[/bold cyan]")

        if user_input.lower() == 'exit':
            break

        # Pass tool_results to the chat function
        response = chat(user_input, conversation_history, current_workspace, tool_results) # {{ edit_1: Pass tool_results to chat }}

        # Handle the response, whether it's a string or a Message object
        assistant_response = response.text if hasattr(response, 'text') else str(response) # {{ edit_1: Access text attribute or convert to string }}

        console.print(f"[bold green]Praxis[/bold green]: {assistant_response}")
        conversation_history.append(f"You: {user_input}")
        conversation_history.append(f"Praxis: {assistant_response}")

        # Update conversation history after each response
        update_conversation_history_tool(f"User: {user_input}\nPraxis: {assistant_response}", current_workspace)

        tool_results = [] # {{ edit_3: Reset tool_results after each user input }}

        # Check if tool_calls exists and is not empty
        if hasattr(response, 'tool_calls') and response.tool_calls: # {{ edit_4: Check for tool_calls attribute }}
            for tool_call in response.tool_calls:
                tool_result = execute_tool(tool_call, current_workspace)
                tool_results.append(tool_result)

                # Update current workspace if it was changed during tool execution
                if "enter_workspace_tool" in str(tool_call): # {{ edit_5: Check tool name within string representation }}
                    current_workspace = tool_result.split("Entered workspace: ")[-1] # {{ edit_6: Extract workspace name }}

            # Get Praxis's response to the tool results
            response = chat(f"Tool execution results: {', '.join(tool_results)}", conversation_history, current_workspace, tool_results) # {{ edit_7: Pass tool_results to chat }}
            assistant_response = response.text if hasattr(response, 'text') else str(response) # {{ edit_2: Access text attribute or convert to string }}

            console.print(f"[bold green]Praxis[/bold green]: {assistant_response}")
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
            tool_args = getattr(tool_call.function, 'arguments', {}) # {{ edit_1: Handle Langchain tools, which have a different structure }}
        elif hasattr(tool_call, 'tool'): # Check for other tool formats
            tool_name = getattr(tool_call.tool, '__name__', str(tool_call.tool))
            tool_args = tool_call.arguments if hasattr(tool_call, 'arguments') else {} # {{ edit_2: Use tool_call.arguments if params doesn't exist }}
        else: # Fallback if tool structure is unknown
            tool_name = str(tool_call) # {{ edit_3: Fallback to string representation if tool structure is unknown }}
            tool_args = {}

        rprint(f"[bold cyan]Executing tool:[/bold cyan] {tool_name}")
        rprint(f"[bold cyan]Arguments:[/bold cyan] {tool_args}")

        # Add current_workspace to the arguments if it's expected by the tool
        if 'current_workspace' in inspect.signature(tool_call).parameters: # {{ edit_4: Use inspect.signature(tool_call) instead of tool_call.tool }}
            tool_args['current_workspace'] = current_workspace

        # Execute the tool based on its structure
        if callable(tool_call): # {{ edit_5: Check if tool_call is callable }}
            result = tool_call(**tool_args)
        elif hasattr(tool_call, 'tool') and callable(tool_call.tool): # {{ edit_6: Check if tool_call.tool is callable }}
            result = tool_call.tool(**tool_args)
        else:
            raise ValueError(f"Unable to execute tool: {tool_name}") # {{ edit_7: Raise exception if tool cannot be executed }}

        rprint(f"[bold green]Tool Execution Result:[/bold green] {result}")
        return result
    except Exception as e:
        error_message = f"Error executing tool: {str(e)}"
        rprint(f"[bold red]Error:[/bold red] {error_message}")
        return error_message

if __name__ == "__main__":
    cli()