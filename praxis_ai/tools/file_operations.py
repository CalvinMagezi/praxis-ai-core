# tools/file_operations.py

import os
from pathlib import Path
from ..utils.logging import logger
from ..workspace_manager import WorkspaceManager

workspace_manager = WorkspaceManager()

def create_folder_structure(workspace_name: str, project_name: str, folder_structure: dict, code_blocks: list):
    workspace_path = workspace_manager.get_workspace_path(workspace_name)
    
    if not workspace_path:
        logger.error(f"No valid workspace path for workspace: {workspace_name}")
        return

    project_path = Path(workspace_path) / project_name

    try:
        project_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created project folder: {project_path}")
    except OSError as e:
        logger.error(f"Error creating project folder: {project_path}. Error: {e}")
        return

    create_folders_and_files(project_path, folder_structure, code_blocks)

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

def read_file(workspace_name: str, file_path: str) -> str:
    workspace_path = workspace_manager.get_workspace_path(workspace_name)
    if not workspace_path:
        logger.error(f"No valid workspace path for workspace: {workspace_name}")
        return ""

    full_path = Path(workspace_path) / file_path
    try:
        with open(full_path, 'r') as file:
            content = file.read()
        return content
    except IOError as e:
        logger.error(f"Error reading file: {full_path}. Error: {e}")
        return ""

def write_file(workspace_name: str, file_path: str, content: str) -> bool:
    workspace_path = workspace_manager.get_workspace_path(workspace_name)
    if not workspace_path:
        logger.error(f"No valid workspace path for workspace: {workspace_name}")
        return False

    full_path = Path(workspace_path) / file_path
    try:
        with open(full_path, 'w') as file:
            file.write(content)
        logger.info(f"File written successfully: {full_path}")
        return True
    except IOError as e:
        logger.error(f"Error writing file: {full_path}. Error: {e}")
        return False