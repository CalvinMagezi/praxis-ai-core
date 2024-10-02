import ell
from ..config.settings import REFINER_MODEL, PRAXIS_NAME
from ..config.models import AgentContext
from ..workspace_manager import WorkspaceManager

workspace_manager = WorkspaceManager()

@ell.complex(model=REFINER_MODEL)
def refiner(context: AgentContext):
    """Praxis AI Refiner that provides the final output."""
    current_workspace = workspace_manager.get_current_workspace()
    workspace_path = workspace_manager.get_workspace_path(current_workspace)

    messages = [
        ell.system(f"You are the refiner for {PRAXIS_NAME}. You are currently working in the '{current_workspace}' workspace "
                   f"located at {workspace_path}. Your role is to review and refine the sub-task results into a cohesive final output. "
                   "Ensure that all outputs are consistent with the current workspace context."),
        ell.user(f"Objective: {context.objective}\n\nSub-task results:\n" + 
                 "\n".join([task.result for task in context.tasks if task.result]) + 
                 "\n\nPlease review and refine the sub-task results into a cohesive final output. "
                 "Add any missing information or details as needed. When working on code projects, "
                 "provide the following only if the project is clearly a coding one:\n"
                 "1. Project Name: Create a concise and appropriate project name (max 20 characters).\n"
                 "2. Folder Structure: Provide the folder structure as a valid JSON object, wrapped in <folder_structure> tags.\n"
                 "3. Code Files: For each code file, include only the file name followed by the code block enclosed in triple backticks.\n"
                 "Remember to consider the current workspace context in your refined output.")
    ]
    return messages