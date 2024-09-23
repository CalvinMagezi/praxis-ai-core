import os
import json
from pathlib import Path
from typing import Dict, Optional, List
from rich.console import Console
from rich.panel import Panel

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