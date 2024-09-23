# core/orchestrator.py

import ell
from config.settings import ORCHESTRATOR_MODEL, PRAXIS_NAME
from config.models import AgentContext
from workspace_manager import WorkspaceManager

workspace_manager = WorkspaceManager()

@ell.complex(model=ORCHESTRATOR_MODEL)
def orchestrator(context: AgentContext):
    """Praxis AI Orchestrator that breaks down objectives into sub-tasks."""
    current_workspace = workspace_manager.get_current_workspace()
    workspace_path = workspace_manager.get_workspace_path(current_workspace)
    
    previous_results_text = "\n".join(context.previous_results) if context.previous_results else "None"
    
    messages = [
        ell.system(f"You are the orchestrator for {PRAXIS_NAME}, a detailed and meticulous AI assistant. "
                   f"You are currently working in the '{current_workspace}' workspace located at {workspace_path}. "
                   "Your primary goal is to break down complex objectives into manageable sub-tasks, provide thorough reasoning, "
                   "and ensure code correctness. Always explain your thought process step-by-step and validate any code for errors, "
                   "improvements, and adherence to best practices."),
        ell.user(f"Based on the following objective and the previous sub-task results (if any), "
                 f"please break down the objective into the next sub-task, and create a concise and detailed prompt for a subagent so it can execute that task. "
                 f"IMPORTANT!!! when dealing with code tasks make sure you check the code for errors and provide fixes and support as part of the next sub-task. "
                 f"If you find any bugs or have suggestions for better code, include them in the next sub-task prompt. "
                 f"Please assess if the objective has been fully achieved. If the previous sub-task results comprehensively address all aspects of the objective, "
                 f"include the phrase 'The task is complete:' at the beginning of your response. If the objective is not yet fully achieved, "
                 f"break it down into the next sub-task and create a concise and detailed prompt for a subagent to execute that task. "
                 f"Remember to consider the current workspace context in your response.\n\n"
                 f"Objective: {context.objective}\n\n"
                 f"Previous sub-task results:\n{previous_results_text}")
    ]

    return messages