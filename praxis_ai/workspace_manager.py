import os
import json
from pathlib import Path
from typing import Dict, Optional, List, Any
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
import time
from rich.progress import Progress, SpinnerColumn, TextColumn

class WorkspaceError(Exception):
    """Custom exception for workspace-related errors."""
    pass

class WorkspaceManager:
    def __init__(self, base_path: str = os.path.expanduser("~/Desktop/PraxisWorkspaces")):
        self.base_path = Path(base_path)
        self.console = Console()
        self.current_workspace: Optional[str] = None
        self.workspaces: Dict[str, Dict] = {}
        self._initialize_workspace_directory()
        self._load_workspaces()

    def _initialize_workspace_directory(self):
        try:
            self.base_path.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            raise WorkspaceError(f"Permission denied when creating directory: {self.base_path}")
        except Exception as e:
            raise WorkspaceError(f"Error creating workspace directory: {e}")

    def _load_workspaces(self):
        workspace_file = self.base_path / "workspaces.json"
        if workspace_file.exists():
            try:
                with open(workspace_file, "r") as f:
                    self.workspaces = json.load(f)
            except json.JSONDecodeError:
                self.console.print("[bold red]Error loading workspaces: Invalid JSON file[/bold red]")
                self.workspaces = {}
            except Exception as e:
                self.console.print(f"[bold red]Error loading workspaces: {e}[/bold red]")
                self.workspaces = {}
        else:
            self.workspaces = {}

    def _save_workspaces(self):
        workspace_file = self.base_path / "workspaces.json"
        try:
            with open(workspace_file, "w") as f:
                json.dump(self.workspaces, f, indent=2)
        except Exception as e:
            raise WorkspaceError(f"Error saving workspaces: {e}")

    def create_workspace(self, title: str, description: str) -> bool:
        if title in self.workspaces:
            raise WorkspaceError(f"Workspace '{title}' already exists")
        
        workspace_path = self.base_path / title
        try:
            workspace_path.mkdir(exist_ok=True)
        except Exception as e:
            raise WorkspaceError(f"Error creating workspace directory: {e}")
        
        self.workspaces[title] = {
            "description": description,
            "path": str(workspace_path)
        }
        self._save_workspaces()
        self.current_workspace = title
        os.chdir(workspace_path)
        return True

    def select_workspace(self, title: str) -> bool:
        if title not in self.workspaces:
            raise WorkspaceError(f"Workspace '{title}' does not exist")
        
        self.current_workspace = title
        try:
            os.chdir(self.workspaces[title]["path"])
        except Exception as e:
            raise WorkspaceError(f"Error changing to workspace directory: {e}")
        return True

    def list_workspaces(self) -> List[Dict[str, str]]:
        return [{"title": title, "description": info["description"]} for title, info in self.workspaces.items()]

    def get_current_workspace(self) -> Optional[str]:
        return self.current_workspace

    def get_workspace_path(self, title: Optional[str] = None) -> Optional[str]:
        if title is None:
            title = self.current_workspace
        return self.workspaces.get(title, {}).get("path")

    def delete_workspace(self, title: str) -> bool:
        if title not in self.workspaces:
            raise WorkspaceError(f"Workspace '{title}' does not exist")
        
        workspace_path = Path(self.workspaces[title]["path"])
        try:
            # Remove all files and subdirectories
            for item in workspace_path.glob('*'):
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    for sub_item in item.glob('*'):
                        sub_item.unlink()
                    item.rmdir()
            workspace_path.rmdir()
        except Exception as e:
            raise WorkspaceError(f"Error deleting workspace directory: {e}")
        
        del self.workspaces[title]
        self._save_workspaces()
        
        if self.current_workspace == title:
            self.current_workspace = None
            os.chdir(self.base_path)
        
        return True

    def save_conversation(self, workspace_name: str, message: str):
        workspace_path = self.get_workspace_path(workspace_name)
        if not workspace_path:
            raise WorkspaceError(f"Workspace '{workspace_name}' does not exist")
        
        conversation_file = Path(workspace_path) / "conversation_log.txt"
        try:
            with open(conversation_file, "a") as f:
                f.write(f"{message}\n")
        except Exception as e:
            raise WorkspaceError(f"Error saving conversation: {e}")

    def load_conversation(self, workspace_name: str) -> List[str]:
        workspace_path = self.get_workspace_path(workspace_name)
        if not workspace_path:
            raise WorkspaceError(f"Workspace '{workspace_name}' does not exist")
        
        conversation_file = Path(workspace_path) / "conversation_log.txt"
        if not conversation_file.exists():
            return []
        
        try:
            with open(conversation_file, "r") as f:
                return f.readlines()
        except Exception as e:
            raise WorkspaceError(f"Error loading conversation: {e}")

    def save_log(self, workspace_name: str, filename: str, content: str):
        workspace_path = self.get_workspace_path(workspace_name)
        if not workspace_path:
            raise WorkspaceError(f"Workspace '{workspace_name}' does not exist")
        
        logs_dir = Path(workspace_path) / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        log_file = logs_dir / filename
        try:
            with open(log_file, "w") as f:
                f.write(content)
        except Exception as e:
            raise WorkspaceError(f"Error saving log: {e}")

    def save_chat(self, workspace_name: str, chat_title: str, content: str):
        workspace_path = self.get_workspace_path(workspace_name)
        if not workspace_path:
            raise WorkspaceError(f"Workspace '{workspace_name}' does not exist")
        
        chats_dir = Path(workspace_path) / "chats"
        chats_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{timestamp}_{chat_title}.md"
        chat_file = chats_dir / filename
        
        try:
            with open(chat_file, "w") as f:
                f.write(content)
        except Exception as e:
            raise WorkspaceError(f"Error saving chat: {e}")

    def list_chats(self, workspace_name: str) -> List[Dict[str, str]]:
        workspace_path = self.get_workspace_path(workspace_name)
        if not workspace_path:
            raise WorkspaceError(f"Workspace '{workspace_name}' does not exist")
        
        chats_dir = Path(workspace_path) / "chats"
        if not chats_dir.exists():
            return []
        
        chats = []
        for chat_file in chats_dir.glob("*.md"):
            chats.append({
                "date": chat_file.stem.split("_")[0],
                "title": "_".join(chat_file.stem.split("_")[1:])
            })
        
        return sorted(chats, key=lambda x: x["date"], reverse=True)

    def load_chat(self, workspace_name: str, chat_title: str) -> Optional[str]:
        workspace_path = self.get_workspace_path(workspace_name)
        if not workspace_path:
            raise WorkspaceError(f"Workspace '{workspace_name}' does not exist")
        
        chats_dir = Path(workspace_path) / "chats"
        if not chats_dir.exists():
            return None
        
        for chat_file in chats_dir.glob("*.md"):
            if chat_title in chat_file.stem:
                try:
                    with open(chat_file, "r") as f:
                        return f.read()
                except Exception as e:
                    raise WorkspaceError(f"Error loading chat: {e}")
        
        return None

    def initialize_workspace_structure(self, workspace_name: str):
        workspace_path = self.get_workspace_path(workspace_name)
        if not workspace_path:
            raise WorkspaceError(f"Workspace '{workspace_name}' does not exist")
        
        folders = {
            "Chat": ["History"],
            "Studio": ["Content"],
            "Automations": ["Connections", "Workflows"],
            "Builder": ["Form"],
            "Memory": []
        }
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            for folder, subfolders in folders.items():
                task = progress.add_task(f"Setting up your {folder}...", total=None)
                folder_path = Path(workspace_path) / folder
                folder_path.mkdir(exist_ok=True)
                
                for subfolder in subfolders:
                    subfolder_path = folder_path / subfolder
                    subfolder_path.mkdir(exist_ok=True)
                
                time.sleep(0.5)  # Add a small delay for visual effect
                progress.update(task, completed=True)
        
        self.console.print("[bold green]Workspace structure initialized successfully![/bold green]")

    def get_all_workspaces(self) -> Dict[str, Dict]:
        return self.workspaces

    def get_base_path(self) -> str:
        return str(self.base_path)

    def create_folder(self, workspace_name: str, folder_name: str) -> bool:
        workspace_path = self.get_workspace_path(workspace_name)
        if not workspace_path:
            raise WorkspaceError(f"Workspace '{workspace_name}' does not exist")
        
        folder_path = Path(workspace_path) / folder_name
        try:
            folder_path.mkdir(parents=True, exist_ok=True)
            self.console.print(f"[green]Folder '{folder_name}' created in workspace '{workspace_name}'[/green]")
            return True
        except Exception as e:
            raise WorkspaceError(f"Error creating folder: {e}")

    def update_workspace_state(self, workspace_name: str, key: str, value: Any) -> bool:
        if workspace_name not in self.workspaces:
            raise WorkspaceError(f"Workspace '{workspace_name}' does not exist")
        
        self.workspaces[workspace_name][key] = value
        self._save_workspaces()
        return True