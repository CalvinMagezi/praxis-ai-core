import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
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
from rich import print as rprint
from rich.text import Text
from rich.syntax import Syntax
import time

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
    pass

@cli.group()
def create():
    """Create new elements (workspace, studio, workflow, or form)"""
    pass

@create.command()
def workspace():
    """Create and initialize a new workspace"""
    console = Console()
    console.print("[bold cyan]Creating a new workspace[/bold cyan]")
    
    title = Prompt.ask("[yellow]Enter workspace title[/yellow]")
    description = Prompt.ask("[yellow]Enter workspace description[/yellow]")
    
    try:
        if workspace_manager.create_workspace(title, description):
            console.print(Panel(f"[green]Workspace '{title}' created successfully.[/green]", border_style="green"))
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("[cyan]Initializing workspace structure...[/cyan]", total=None)
                workspace_manager.initialize_workspace_structure(title)
                progress.update(task, completed=True)
            
            console.print("[bold green]Workspace initialized successfully![/bold green]")
            console.print(f"[yellow]You can now enter your workspace by typing:[/yellow] praxis enter '{title}'")
    except WorkspaceError as e:
        console.print(Panel(f"[red]Error: {str(e)}[/red]", border_style="red"))

@create.command()
@click.pass_context
def studio(ctx):
    """Create a new studio within the current workspace"""
    if not workspace_manager.get_current_workspace():
        console.print("[red]Error: You must be in a workspace to create a studio.[/red]")
        ctx.abort()
    # Implement studio creation logic here
    console.print("[green]Studio created successfully![/green]")

@create.command()
@click.pass_context
def workflow(ctx):
    """Create a new workflow within the current workspace"""
    if not workspace_manager.get_current_workspace():
        console.print("[red]Error: You must be in a workspace to create a workflow.[/red]")
        ctx.abort()
    # Implement workflow creation logic here
    console.print("[green]Workflow created successfully![/green]")

@create.command()
@click.pass_context
def form(ctx):
    """Create a new form within the current workspace"""
    if not workspace_manager.get_current_workspace():
        console.print("[red]Error: You must be in a workspace to create a form.[/red]")
        ctx.abort()
    # Implement form creation logic here
    console.print("[green]Form created successfully![/green]")

@cli.command()
@click.argument('workspace_name')
def enter(workspace_name):
    """Enter an existing workspace"""
    try:
        workspace_manager.select_workspace(workspace_name)
        console.clear()
        console.print(Panel(f"[bold green]{workspace_name}[/bold green]", 
                            expand=False, border_style="bold", box=box.DOUBLE))
        workspace_cli()
    except WorkspaceError as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@cli.command()
@click.argument('workspace_name')
def delete(workspace_name):
    """Delete a specific workspace"""
    if click.confirm(f"Are you sure you want to delete the workspace '{workspace_name}'? All files and folders within the workspace will be permanently deleted.", abort=True):
        try:
            workspace_manager.delete_workspace(workspace_name)
            console.print(f"[green]Workspace '{workspace_name}' has been deleted.[/green]")
        except WorkspaceError as e:
            console.print(f"[red]Error: {str(e)}[/red]")

def workspace_cli():
    """CLI for operations within a workspace"""
    while True:
        command = Prompt.ask(
            "Enter command",
            choices=["chat", "obj", "objective", "history", "create studio", "create workflow", "create form", "exit"]
        )
        
        if command == "chat":
            start_chat_mode(workspace_manager.get_current_workspace())
        elif command in ["obj", "objective"]:
            objective = Prompt.ask("Enter your objective")
            handle_objective(objective, workspace_manager.get_current_workspace())
        elif command == "history":
            show_history()
        elif command.startswith("create"):
            _, create_type = command.split(" ", 1)
            if create_type == "studio":
                create.invoke(click.Context(create), ["studio"])
            elif create_type == "workflow":
                create.invoke(click.Context(create), ["workflow"])
            elif create_type == "form":
                create.invoke(click.Context(create), ["form"])
        elif command == "exit":
            break

def show_history():
    """Show conversation history for the current workspace"""
    workspace = workspace_manager.get_current_workspace()
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
    
    with console.status("[bold yellow]Analyzing objective...[/bold yellow]") as status:  # Updated status message
        while True:
            status.update("[bold yellow]Breaking down tasks...[/bold yellow]")  # New status update
            orchestrator_response = orchestrator(context)
            orchestrator_text = orchestrator_response.text
            console.print(Panel(Markdown(orchestrator_text), border_style="yellow"))

            if "The task is complete:" in orchestrator_text:
                break

            task = create_task(orchestrator_text)
            context.tasks.append(task)

            status.update(f"[bold cyan]Working on: {task.description[:30]}...[/bold cyan]")  # Updated status message
            sub_agent_response = sub_agent(task, context.tasks)
            sub_agent_text = sub_agent_response.text
            console.print(Panel(Markdown(sub_agent_text), border_style="cyan"))

            task.result = sub_agent_text
            task.status = "completed"
            context.previous_results.append(sub_agent_text)

            status.update("[bold yellow]Evaluating progress...[/bold yellow]")  # New status update

    status.update("[bold green]Finalizing results...[/bold green]")  # New status update
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

@cli.command()
def list():
    """List all available workspaces"""
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

@cli.command()
def main():
    """Display available commands"""
    praxis_text = Text()
    praxis_text.append("  ____                 _     \n", style="bold cyan")
    praxis_text.append(" |  _ \\ _ __ __ ___  _(_)___ \n", style="bold cyan")
    praxis_text.append(" | |_) | '__/ _` \\ \\/ / / __|\n", style="bold cyan")
    praxis_text.append(" |  __/| | | (_| |>  <| \\__ \\\n", style="bold cyan")
    praxis_text.append(" |_|   |_|  \\__,_/_/\\_\\_|___/\n", style="bold cyan")
    praxis_text.append("\nYour Intelligent Workspace Assistant", style="italic yellow")
    
    console.print(Panel(praxis_text, expand=False, border_style="bold"))

    table = Table(title="Available Commands", show_header=True, header_style="bold magenta")
    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")
    table.add_column("Example", style="yellow")

    table.add_row(
        "list",
        "List all available workspaces",
        "praxis list"
    )
    table.add_row(
        "create workspace",
        "Create and initialize a new workspace",
        "praxis create workspace"
    )
    table.add_row(
        "enter",
        "Enter an existing workspace",
        "praxis enter 'My Workspace'"
    )
    table.add_row(
        "delete",
        "Delete a specific workspace",
        "praxis delete 'Old Workspace'"
    )

    console.print(table)

    console.print("\n[bold]Usage Examples:[/bold]")
    examples = """
    # List all workspaces
    $ praxis list

    # Create a new workspace
    $ praxis create workspace

    # Enter an existing workspace
    $ praxis enter "My Project Workspace"

    # Delete a workspace (with confirmation)
    $ praxis delete "Outdated Workspace"

    # Get help for a specific command
    $ praxis create --help
    """
    console.print(Syntax(examples, "bash", theme="monokai", line_numbers=True))

    console.print("\n[bold yellow]Note:[/bold yellow] Use 'praxis [command] --help' for more information on a specific command.")

if __name__ == "__main__":
    cli()