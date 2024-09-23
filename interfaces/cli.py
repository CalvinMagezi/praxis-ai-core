# interfaces/cli.py

import ell
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.markdown import Markdown
from typing import List, Optional
from datetime import datetime
import re

from config.models import AgentContext, Task
from core.orchestrator import orchestrator
from core.sub_agent import sub_agent
from core.refiner import refiner
from utils.helpers import sanitize_string, parse_folder_structure, extract_code_blocks, create_task
from tools.file_operations import create_folder_structure
from workspace_manager import WorkspaceManager, WorkspaceError

console = Console()
workspace_manager = WorkspaceManager()

def run_cli():
    ell.init(store='./ell_logdir', autocommit=True)
    
    console.print(Panel.fit(
        "[bold cyan]Welcome to Praxis AI[/bold cyan]\n"
        "Your intelligent workspace assistant",
        border_style="bold",
        padding=(1, 1),
        title="Praxis AI",
        subtitle="v0.0.1"
    ))
    
    while True:
        if not workspace_manager.get_current_workspace():
            handle_workspace_selection()
        
        console.print(f"\nCurrent workspace: [bold green]{workspace_manager.get_current_workspace()}[/bold green]")
        
        command_table = Table(show_header=False, box=None)
        command_table.add_column("Command", style="cyan")
        command_table.add_column("Description", style="yellow")
        command_table.add_row("objective", "Enter a new objective for Praxis AI")
        command_table.add_row("new workspace", "Create a new workspace")
        command_table.add_row("switch workspace", "Switch to a different workspace")
        command_table.add_row("delete workspace", "Delete the current workspace")
        command_table.add_row("list workspaces", "List all available workspaces")
        command_table.add_row("quit", "Exit Praxis AI")
        
        console.print(command_table)
        
        action = Prompt.ask(
            "\nEnter command",
            choices=["objective", "new workspace", "switch workspace", "delete workspace", "list workspaces", "quit"],
            default="objective"
        )

        if action == "quit":
            console.print("[yellow]Thank you for using Praxis AI. Goodbye![/yellow]")
            break
        elif action == "new workspace":
            handle_workspace_creation()
        elif action == "switch workspace":
            handle_workspace_selection()
        elif action == "delete workspace":
            handle_workspace_deletion()
        elif action == "list workspaces":
            list_workspaces()
        elif action == "objective":
            handle_objective()


def handle_workspace_creation():
    title = Prompt.ask("Enter workspace title")
    description = Prompt.ask("Enter workspace description")
    try:
        if workspace_manager.create_workspace(title, description):
            console.print(Panel(f"[green]Workspace '{title}' created successfully.[/green]", border_style="green"))
    except WorkspaceError as e:
        console.print(Panel(f"[red]Error: {str(e)}[/red]", border_style="red"))

def handle_workspace_selection():
    workspaces = workspace_manager.list_workspaces()
    if not workspaces:
        console.print("[yellow]No workspaces found. Please create a new workspace.[/yellow]")
        handle_workspace_creation()
        return

    table = Table(title="Available Workspaces")
    table.add_column("Title", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")

    for workspace in workspaces:
        table.add_row(workspace["title"], workspace["description"])

    console.print(table)

    while True:
        selected = Prompt.ask("Enter the title of the workspace you want to use")
        try:
            if workspace_manager.select_workspace(selected):
                console.print(Panel(f"[green]Switched to workspace '{selected}'.[/green]", border_style="green"))
                break
        except WorkspaceError as e:
            console.print(Panel(f"[red]Error: {str(e)}[/red]", border_style="red"))

def handle_workspace_deletion():
    current_workspace = workspace_manager.get_current_workspace()
    if current_workspace:
        if Prompt.ask(f"Are you sure you want to delete the current workspace '{current_workspace}'?", choices=["y", "n"]) == "y":
            try:
                if workspace_manager.delete_workspace(current_workspace):
                    console.print(Panel(f"[green]Workspace '{current_workspace}' deleted successfully.[/green]", border_style="green"))
            except WorkspaceError as e:
                console.print(Panel(f"[red]Error: {str(e)}[/red]", border_style="red"))
    else:
        console.print("[yellow]No workspace is currently selected.[/yellow]")

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

def handle_objective():
    objective = Prompt.ask("Please enter your objective")

    context = AgentContext(objective=objective)
    
    with console.status("[bold green]Processing objective...[/bold green]") as status:
        while True:
            orchestrator_response = orchestrator(context)
            orchestrator_text = orchestrator_response.text
            console.print(Panel(Markdown(orchestrator_text), title="[bold green]Orchestrator[/bold green]", border_style="green"))

            if "The task is complete:" in orchestrator_text:
                break

            task = create_task(orchestrator_text)
            context.tasks.append(task)

            sub_agent_response = sub_agent(task, context.tasks)
            sub_agent_text = sub_agent_response.text
            console.print(Panel(Markdown(sub_agent_text), title="[bold blue]Sub-agent Result[/bold blue]", border_style="blue"))

            task.result = sub_agent_text
            task.status = "completed"
            context.previous_results.append(sub_agent_text)

            status.update(f"[bold green]Processing task {len(context.tasks)}...[/bold green]")

    refiner_response = refiner(context)
    refined_output = refiner_response.text

    console.print("\n[bold]Refined Final output:[/bold]")
    console.print(Panel(Markdown(refined_output), title="[bold purple]Refined Output[/bold purple]", border_style="purple"))

    project_name_match = re.search(r'Project Name: (.*)', refined_output)
    project_name = project_name_match.group(1).strip() if project_name_match else sanitize_string(objective)

    folder_structure = parse_folder_structure(refined_output)
    code_blocks = extract_code_blocks(refined_output)
    create_folder_structure(project_name, folder_structure, code_blocks)

    save_log(objective, context, refined_output)

def save_log(objective: str, context: AgentContext, refined_output: str):
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
        with open(filename, 'w') as file:
            file.write(log_content)
        console.print(f"\n[green]Full exchange log saved to {filename}[/green]")
    except Exception as e:
        console.print(f"\n[red]Error saving log file: {str(e)}[/red]")