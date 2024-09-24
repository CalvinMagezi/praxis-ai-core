# core/sub_agent.py

import ell
from ..config.settings import SUB_AGENT_MODEL, PRAXIS_NAME
from ..config.models import Task
from ..workspace_manager import WorkspaceManager
from typing import List

workspace_manager = WorkspaceManager()

@ell.complex(model=SUB_AGENT_MODEL)
def sub_agent(task: Task, previous_tasks: List[Task] = None):
    """Praxis AI Sub-agent that executes specific tasks."""
    if previous_tasks is None:
        previous_tasks = []

    current_workspace = workspace_manager.get_current_workspace()
    workspace_path = workspace_manager.get_workspace_path(current_workspace)

    system_message = (
        f"You are an expert sub-agent for {PRAXIS_NAME}. You are currently working in the '{current_workspace}' workspace "
        f"located at {workspace_path}. Your goal is to execute tasks accurately, provide detailed explanations of your reasoning, "
        "and ensure the correctness and quality of any code. Always explain your thought process and validate your output thoroughly. "
        "When dealing with files or paths, make sure to use the correct workspace path.\n\n"
        "Previous tasks:\n" + "\n".join(f"Task: {task.description}\nResult: {task.result}" for task in previous_tasks)
    )
    
    messages = [
        ell.system(system_message),
        ell.user(task.description)
    ]

    return messages