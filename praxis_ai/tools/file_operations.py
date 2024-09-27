# tools/file_operations.py

import ell
import os
from pathlib import Path
from ..utils.logging import logger
from ..workspace_manager import WorkspaceManager, WorkspaceError

workspace_manager = WorkspaceManager()

@ell.tool()
def read_file_tool(file_path: str, current_workspace: str) -> str:
    """
    Read the contents of a file in the specified workspace.

    Args:
    file_path (str): The path to the file within the workspace.
    current_workspace (str): The name of the current workspace.

    Returns:
    str: The contents of the file, or an error message if the file cannot be read.
    """
    workspace_path = workspace_manager.get_workspace_path(current_workspace)
    if not workspace_path:
        return f"Error: No valid workspace path for workspace: {current_workspace}"

    full_path = Path(workspace_path) / file_path
    try:
        with open(full_path, 'r') as file:
            content = file.read()
        return content
    except IOError as e:
        error_message = f"Error reading file: {full_path}. Error: {e}"
        logger.error(error_message)
        return error_message

@ell.tool()
def write_file_tool(file_path: str, content: str, current_workspace: str) -> str:
    """
    Write content to a file in the specified workspace.

    Args:
    file_path (str): The path to the file within the workspace.
    content (str): The content to write to the file.
    current_workspace (str): The name of the current workspace.

    Returns:
    str: A success message, or an error message if the file cannot be written.
    """
    workspace_path = workspace_manager.get_workspace_path(current_workspace)
    if not workspace_path:
        return f"Error: No valid workspace path for workspace: {current_workspace}"

    full_path = Path(workspace_path) / file_path
    try:
        with open(full_path, 'w') as file:
            file.write(content)
        success_message = f"File written successfully: {full_path}"
        logger.info(success_message)
        return success_message
    except IOError as e:
        error_message = f"Error writing file: {full_path}. Error: {e}"
        logger.error(error_message)
        return error_message

@ell.tool()
def create_folder_structure_tool(project_name: str, folder_structure: dict, code_blocks: list, current_workspace: str) -> str:
    """
    Create a folder structure with files in the specified workspace.

    Args:
    project_name (str): The name of the project (root folder).
    folder_structure (dict): A dictionary representing the folder structure.
    code_blocks (list): A list of tuples containing file names and their content.
    current_workspace (str): The name of the current workspace.

    Returns:
    str: A success message, or an error message if the structure cannot be created.
    """
    workspace_path = workspace_manager.get_workspace_path(current_workspace)
    if not workspace_path:
        return f"Error: No valid workspace path for workspace: {current_workspace}"

    project_path = Path(workspace_path) / project_name

    try:
        project_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created project folder: {project_path}")
    except OSError as e:
        error_message = f"Error creating project folder: {project_path}. Error: {e}"
        logger.error(error_message)
        return error_message

    def create_folders_and_files(current_path: Path, structure: dict, code_blocks: list):
        for key, value in structure.items():
            path = current_path / key
            if isinstance(value, dict):
                try:
                    path.mkdir(exist_ok=True)
                    logger.info(f"Created folder: {path}")
                    create_folders_and_files(path, value, code_blocks)
                except OSError as e:
                    logger.error(f"Error creating folder: {path}. Error: {e}")
            else:
                code_content = next((code for file, code in code_blocks if file == key), None)
                if code_content:
                    try:
                        with open(path, 'w') as file:
                            file.write(code_content)
                        logger.info(f"Created file: {path}")
                    except IOError as e:
                        logger.error(f"Error creating file: {path}. Error: {e}")
                else:
                    logger.warning(f"Code content not found for file: {key}")

    create_folders_and_files(project_path, folder_structure, code_blocks)
    return f"Folder structure created for project '{project_name}' in workspace '{current_workspace}'"