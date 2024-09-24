# utils/helpers.py

import re
import json
import uuid
from typing import List, Tuple
from ..config.models import Task
from .logging import logger
from ..workspace_manager import WorkspaceManager

workspace_manager = WorkspaceManager()

def sanitize_string(s: str) -> str:
    return re.sub(r'\W+', '_', s)

def parse_folder_structure(refined_output: str) -> dict:
    folder_structure_match = re.search(r'<folder_structure>(.*?)</folder_structure>', refined_output, re.DOTALL)
    if folder_structure_match:
        json_string = folder_structure_match.group(1).strip()
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON: {e}")
            logger.error(f"Invalid JSON string: {json_string}")
    return {}

def extract_code_blocks(refined_output: str) -> List[Tuple[str, str]]:
    return re.findall(r'Filename: (\S+)\s*```[\w]*\n(.*?)\n```', refined_output, re.DOTALL)

def create_task(description: str) -> Task:
    return Task(id=str(uuid.uuid4()), description=description, status="pending")

def get_workspace_file_path(filename: str) -> str:
    current_workspace = workspace_manager.get_current_workspace()
    workspace_path = workspace_manager.get_workspace_path(current_workspace)
    return str(workspace_path / filename) if workspace_path else filename