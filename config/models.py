# config/models.py

from pydantic import BaseModel, Field
from typing import List, Optional

class Task(BaseModel):
    id: str
    description: str
    status: str
    result: Optional[str] = None

class AgentContext(BaseModel):
    objective: str
    previous_results: List[str] = Field(default_factory=list)
    tasks: List[Task] = Field(default_factory=list)