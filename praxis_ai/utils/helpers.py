import re
import json
import uuid
from typing import List, Tuple, Optional, Dict, Any
from ..config.models import Task
from .logging import logger
from ..workspace_manager import WorkspaceManager
from pathlib import Path

workspace_manager = WorkspaceManager()

def sanitize_string(s: str) -> str:
    """Sanitize a string by replacing non-word characters with underscores."""
    return re.sub(r'\W+', '_', s)

def parse_folder_structure(refined_output: str) -> Dict[str, Any]:
    """Parse the folder structure from the refined output."""
    folder_structure_match = re.search(r'<folder_structure>(.*?)</folder_structure>', refined_output, re.DOTALL)
    if folder_structure_match:
        json_string = folder_structure_match.group(1).strip()
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON: {e}")
            logger.error(f"Invalid JSON string: {json_string}")
            return {}
    logger.warning("No folder structure found in refined output.")
    return {}

def extract_code_blocks(refined_output: str) -> List[Tuple[str, str]]:
    """Extract code blocks from the refined output."""
    code_blocks = re.findall(r'Filename: (\S+)\s*```[\w]*\n(.*?)\n```', refined_output, re.DOTALL)
    if not code_blocks:
        logger.warning("No code blocks found in refined output.")
    return code_blocks

def create_task(description: str) -> Task:
    """Create a new task with a unique ID."""
    return Task(id=str(uuid.uuid4()), description=description, status="pending")

def get_workspace_file_path(filename: str) -> Optional[Path]:
    """Get the full file path in the current workspace."""
    current_workspace = workspace_manager.get_current_workspace()
    workspace_path = workspace_manager.get_workspace_path(current_workspace)
    if workspace_path:
        return Path(workspace_path) / filename
    logger.warning(f"No valid workspace path for file: {filename}")
    return None

def safe_json_loads(json_string: str) -> Dict[str, Any]:
    """Safely load a JSON string, returning an empty dict if parsing fails."""
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON: {e}")
        logger.error(f"Invalid JSON string: {json_string}")
        return {}

def ensure_directory_exists(path: Path) -> None:
    """Ensure that a directory exists, creating it if necessary."""
    try:
        path.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        logger.error(f"Permission denied when creating directory: {path}")
    except Exception as e:
        logger.error(f"Error creating directory {path}: {e}")

def safe_write_file(file_path: Path, content: str) -> bool:
    """Safely write content to a file, returning True if successful."""
    try:
        with file_path.open('w', encoding='utf-8') as f:
            f.write(content)
        return True
    except IOError as e:
        logger.error(f"Error writing to file {file_path}: {e}")
        return False

def safe_read_file(file_path: Path) -> Optional[str]:
    """Safely read content from a file, returning None if unsuccessful."""
    try:
        with file_path.open('r', encoding='utf-8') as f:
            return f.read()
    except IOError as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return None

def validate_workspace_name(name: str) -> bool:
    """Validate a workspace name."""
    return bool(re.match(r'^[\w-]+$', name))

def get_project_name_from_output(refined_output: str) -> Optional[str]:
    """Extract the project name from the refined output."""
    match = re.search(r'Project Name: (.+)', refined_output)
    if match:
        return match.group(1).strip()
    logger.warning("No project name found in refined output.")
    return None