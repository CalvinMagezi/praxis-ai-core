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
                 "ONLY AND ONLY IF THE PROJECT IS CLEARLY A CODING ONE please provide the following:\n"
                 "1. Project Name: Create a concise and appropriate project name that fits the project based on what it's creating. "
                 "The project name should be no more than 20 characters long.\n"
                 "2. Folder Structure: Provide the folder structure as a valid JSON object, where each key represents a folder or file, "
                 "and nested keys represent subfolders. Use null values for files. Ensure the JSON is properly formatted without any syntax errors. "
                 "Please make sure all keys are enclosed in double quotes, and ensure objects are correctly encapsulated with braces, "
                 "separating items with commas as necessary. Wrap the JSON object in <folder_structure> tags.\n"
                 "3. Code Files: For each code file, include ONLY the file name NEVER EVER USE THE FILE PATH OR ANY OTHER FORMATTING "
                 "YOU ONLY USE THE FOLLOWING format 'Filename: <filename>' followed by the code block enclosed in triple backticks, "
                 "with the language identifier after the opening backticks, like this:\n\n```python\n<code>\n```\n"
                 "Remember to consider the current workspace context in your refined output.")
    ]
    return messages