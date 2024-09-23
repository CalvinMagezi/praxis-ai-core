# interfaces/api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from config.models import AgentContext
from core.orchestrator import orchestrator
from core.sub_agent import sub_agent
from core.refiner import refiner
from utils.helpers import create_task

app = FastAPI()

class ObjectiveRequest(BaseModel):
    objective: str
    file_content: str = None

class TaskResponse(BaseModel):
    task_id: str
    description: str
    status: str

class FinalResponse(BaseModel):
    objective: str
    refined_output: str

@app.post("/objective", response_model=List[TaskResponse])
async def process_objective(request: ObjectiveRequest):
    context = AgentContext(objective=request.objective, file_content=request.file_content)
    
    tasks = []
    while True:
        orchestrator_response = orchestrator(context)
        orchestrator_text = orchestrator_response.text

        if "The task is complete:" in orchestrator_text:
            break

        task = create_task(orchestrator_text)
        context.tasks.append(task)
        tasks.append(TaskResponse(task_id=task.id, description=task.description, status=task.status))

        sub_agent_response = sub_agent(task, context.tasks)
        sub_agent_text = sub_agent_response.text

        task.result = sub_agent_text
        task.status = "completed"
        context.previous_results.append(sub_agent_text)

    return tasks

@app.get("/task/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    # Implement task retrieval logic
    # This is a placeholder implementation
    return TaskResponse(task_id=task_id, description="Task description", status="completed")

@app.post("/refine", response_model=FinalResponse)
async def refine_results(context: AgentContext):
    refiner_response = refiner(context)
    refined_output = refiner_response.text

    return FinalResponse(objective=context.objective, refined_output=refined_output)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)