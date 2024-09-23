# tests/test_orchestrator.py

import pytest
from config.models import AgentContext
from core.orchestrator import orchestrator

def test_orchestrator():
    context = AgentContext(objective="Test objective")
    response = orchestrator(context)
    
    assert response is not None
    assert isinstance(response.text, str)
    assert len(response.text) > 0

def test_orchestrator_with_file_content():
    context = AgentContext(objective="Test objective", file_content="Sample file content")
    response = orchestrator(context)
    
    assert response is not None
    assert isinstance(response.text, str)
    assert len(response.text) > 0
    assert "file content" in response.text.lower()

def test_orchestrator_task_completion():
    context = AgentContext(objective="Test objective", previous_results=["Task 1 completed", "Task 2 completed"])
    response = orchestrator(context)
    
    assert response is not None
    assert isinstance(response.text, str)
    assert "The task is complete:" in response.text or len(context.tasks) > 0