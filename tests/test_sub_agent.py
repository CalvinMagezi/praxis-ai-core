# tests/test_sub_agent.py

import pytest
from config.models import Task
from core.sub_agent import sub_agent

def test_sub_agent():
    task = Task(id="1", description="Test task", status="pending")
    response = sub_agent(task)
    
    assert response is not None
    assert isinstance(response.text, str)
    assert len(response.text) > 0

def test_sub_agent_with_previous_tasks():
    previous_tasks = [
        Task(id="1", description="Previous task 1", status="completed", result="Result 1"),
        Task(id="2", description="Previous task 2", status="completed", result="Result 2")
    ]
    current_task = Task(id="3", description="Current task", status="pending")
    
    response = sub_agent(current_task, previous_tasks)
    
    assert response is not None
    assert isinstance(response.text, str)
    assert len(response.text) > 0
    assert "Previous task" in response.text