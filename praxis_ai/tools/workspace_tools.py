# tools/workspace_tools.py

import ell
from ..workspace_manager import WorkspaceManager, WorkspaceError

workspace_manager = WorkspaceManager()

@ell.tool()
def create_workspace_tool(title: str, description: str):
    """Create a new workspace with the given title and description."""
    try:
        workspace_manager.create_workspace(title, description)
        return f"Workspace '{title}' created successfully."
    except WorkspaceError as e:
        return f"Error creating workspace: {str(e)}"

@ell.tool()
def list_workspaces_tool():
    """List all available workspaces."""
    workspaces = workspace_manager.list_workspaces()
    return "\n".join([f"- {w['title']}: {w['description']}" for w in workspaces])

@ell.tool()
def enter_workspace_tool(title: str):
    """Enter the specified workspace."""
    try:
        workspace_manager.select_workspace(title)
        return f"Entered workspace: {title}"
    except WorkspaceError as e:
        return f"Error entering workspace: {str(e)}"

@ell.tool()
def delete_workspace_tool(title: str):
    """Delete the specified workspace."""
    try:
        workspace_manager.delete_workspace(title)
        return f"Workspace '{title}' deleted successfully."
    except WorkspaceError as e:
        return f"Error deleting workspace: {str(e)}"

@ell.tool()
def create_folder_tool(workspace_name: str, folder_name: str):
    """Create a new folder in the specified workspace."""
    try:
        workspace_manager.create_folder(workspace_name, folder_name)
        return f"Folder '{folder_name}' created in workspace '{workspace_name}'."
    except WorkspaceError as e:
        return f"Error creating folder: {str(e)}"