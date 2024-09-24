import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich import box
from typing import Optional, List
from datetime import datetime
import re
import os

import ell
from openai import OpenAI
from .config.models import AgentContext
from .core.orchestrator import orchestrator
from .core.sub_agent import sub_agent
from .core.refiner import refiner
from .core.chat import chat  # Import the new chat function
from .utils.helpers import sanitize_string, parse_folder_structure, extract_code_blocks, create_task
from .tools.file_operations import create_folder_structure
from .workspace_manager import WorkspaceManager, WorkspaceError
from .config.settings import CHAT_MODEL  # Import the CHAT_MODEL setting

console = Console()
workspace_manager = WorkspaceManager()

def check_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print("[yellow]No OpenAI API key found in environment variables.[/yellow]")
        api_key = Prompt.ask("Please enter your OpenAI API key")
        os.environ["OPENAI_API_KEY"] = api_key
        console.print("[green]API key set successfully.[/green]")
    return api_key

@click.group()
def cli():
    """Praxis AI - Your intelligent workspace assistant"""
    api_key = check_api_key()
    ell.init(store='./ell_logdir', autocommit=True)
    
    # Register the OpenAI client for all models we're using
    openai_client = OpenAI(api_key=api_key)
    ell.config.register_model("gpt-4o", openai_client)
    ell.config.register_model("gpt-4o-mini", openai_client)
    # Add any other models you're using in your application

@cli.command()
def list():
    """List all available workspaces"""
    list_workspaces()

@cli.command()
@click.argument('workspace_name', nargs=-1, required=False)
def enter(workspace_name: tuple):
    """Enter a workspace and start chat mode"""
    workspace_name = ' '.join(workspace_name) if workspace_name else None
    
    if not workspace_name:
        workspaces = workspace_manager.list_workspaces()
        if not workspaces:
            console.print("[yellow]No workspaces found. Creating a new one.[/yellow]")
            create_new_workspace()
        else:
            list_workspaces()
            workspace_name = Prompt.ask("Enter the name of the workspace you want to enter")
    
    try:
        workspace_manager.select_workspace(workspace_name)
        console.clear()
        console.print(Panel(f"[bold green]{workspace_name}[/bold green]", 
                            expand=False, border_style="bold", box=box.DOUBLE))
        start_chat_mode(workspace_name)
    except WorkspaceError as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if Prompt.ask("Would you like to create a new workspace?", choices=["y", "n"]) == "y":
            create_new_workspace()

@cli.command()
@click.option('--workspace', help='Workspace name to show history for')
def history(workspace: Optional[str] = None):
    """Show conversation history for a workspace"""
    if not workspace:
        workspace = workspace_manager.get_current_workspace()
        if not workspace:
            console.print("[yellow]No workspace selected. Please enter a workspace first.[/yellow]")
            return
    
    chats = workspace_manager.list_chats(workspace)
    if not chats:
        console.print(f"[yellow]No chat history found for workspace '{workspace}'.[/yellow]")
        return

    table = Table(title=f"Chat History for {workspace}")
    table.add_column("Date", style="cyan")
    table.add_column("Title", style="magenta")

    for chat in chats:
        table.add_row(chat['date'], chat['title'])

    console.print(table)

    chat_to_view = Prompt.ask("Enter the title of the chat you want to view (or press Enter to skip)")
    if chat_to_view:
        chat_content = workspace_manager.load_chat(workspace, chat_to_view)
        if chat_content:
            console.print(Panel(Markdown(chat_content), title=chat_to_view, border_style="green"))
        else:
            console.print(f"[yellow]Chat '{chat_to_view}' not found.[/yellow]")

def create_new_workspace():
    title = Prompt.ask("Enter workspace title")
    description = Prompt.ask("Enter workspace description")
    try:
        if workspace_manager.create_workspace(title, description):
            console.print(Panel(f"[green]Workspace '{title}' created successfully.[/green]", border_style="green"))
            start_chat_mode(title)
    except WorkspaceError as e:
        console.print(Panel(f"[red]Error: {str(e)}[/red]", border_style="red"))

def list_workspaces():
    workspaces = workspace_manager.list_workspaces()
    if not workspaces:
        console.print("[yellow]No workspaces found.[/yellow]")
        return

    table = Table(title="Praxis AI Workspaces")
    table.add_column("Title", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")

    for workspace in workspaces:
        table.add_row(workspace["title"], workspace["description"])

    console.print(table)

def start_chat_mode(workspace_name: str):
    console.print("[bold green]Entering chat mode for workspace: [/bold green]" + workspace_name)
    console.print("Type 'exit' to leave the workspace, or 'objective: <your objective>' to start a new objective.")
    
    conversation_history = workspace_manager.load_conversation(workspace_name)
    if conversation_history:
        console.print("[italic]Previous conversation:[/italic]")
        for message in conversation_history[-5:]:  # Show last 5 messages
            console.print(message.strip())
    
    chat_title = None
    
    while True:
        user_input = Prompt.ask("[bold cyan]You[/bold cyan]")
        if user_input.lower() == 'exit':
            break
        elif user_input.lower().startswith('objective:'):
            objective = user_input[len('objective:'):].strip()
            handle_objective(objective, workspace_name)
        else:
            response = chat_with_praxis(user_input, conversation_history, workspace_name)
            console.print(f"[bold green]Praxis[/bold green]: {response}")
            
            conversation_history.append(f"You: {user_input}")
            conversation_history.append(f"Praxis: {response}")
            
            if not chat_title:
                chat_title = user_input[:20] + "..."  # First 20 characters of the first message
    
    if conversation_history:
        workspace_manager.save_chat(workspace_name, chat_title, "\n".join(conversation_history))

def chat_with_praxis(user_input: str, conversation_history: List[str], workspace_name: str) -> str:
    response = chat(user_input, conversation_history, workspace_name)
    return response.text  # Assuming the response is a Message object with a 'text' attribute

def handle_objective(objective: str, workspace_name: str):
    context = AgentContext(objective=objective)
    
    console.print(Panel(f"[bold]Objective:[/bold] {objective}", border_style="blue"))
    
    with console.status("[bold yellow]Thinking hard...[/bold yellow]") as status:
        while True:
            orchestrator_response = orchestrator(context)
            orchestrator_text = orchestrator_response.text
            console.print(Panel(Markdown(orchestrator_text), border_style="yellow"))

            if "The task is complete:" in orchestrator_text:
                break

            task = create_task(orchestrator_text)
            context.tasks.append(task)

            status.update("[bold cyan]Thinking fast...[/bold cyan]")
            sub_agent_response = sub_agent(task, context.tasks)
            sub_agent_text = sub_agent_response.text
            console.print(Panel(Markdown(sub_agent_text), border_style="cyan"))

            task.result = sub_agent_text
            task.status = "completed"
            context.previous_results.append(sub_agent_text)

            status.update("[bold yellow]Thinking hard...[/bold yellow]")

    refiner_response = refiner(context)
    refined_output = refiner_response.text

    console.print("\n[bold]Final output:[/bold]")
    console.print(Panel(Markdown(refined_output), border_style="green"))

    project_name_match = re.search(r'Project Name: (.*)', refined_output)
    project_name = project_name_match.group(1).strip() if project_name_match else sanitize_string(objective)

    folder_structure = parse_folder_structure(refined_output)
    code_blocks = extract_code_blocks(refined_output)
    create_folder_structure(workspace_name, project_name, folder_structure, code_blocks)

    save_log(objective, context, refined_output, workspace_name)

def save_log(objective: str, context: AgentContext, refined_output: str, workspace_name: str):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    sanitized_objective = sanitize_string(objective)
    max_length = 25
    truncated_objective = sanitized_objective[:max_length] if len(sanitized_objective) > max_length else sanitized_objective
    filename = f"{timestamp}_{truncated_objective}.md"

    log_content = f"# Objective: {objective}\n\n"
    log_content += "## Task Breakdown\n\n"
    for i, task in enumerate(context.tasks, start=1):
        log_content += f"### Task {i}:\n"
        log_content += f"**Description:** {task.description}\n\n"
        log_content += f"**Result:** {task.result}\n\n"

    log_content += "## Refined Final Output\n\n"
    log_content += refined_output

    try:
        workspace_manager.save_log(workspace_name, filename, log_content)
        console.print(f"\n[green]Full exchange log saved to {filename}[/green]")
    except Exception as e:
        console.print(f"\n[red]Error saving log file: {str(e)}[/red]")

def main():
    cli()

if __name__ == "__main__":
    main()