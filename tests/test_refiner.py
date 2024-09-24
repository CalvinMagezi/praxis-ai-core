# tests/test_refiner.py

import pytest
from config.models import AgentContext, Task
from core.refiner import refiner

def test_refiner():
    context = AgentContext(
        objective="Test objective",
        tasks=[
            Task(id="1", description="Task 1", status="completed", result="Result 1"),
            Task(id="2", description="Task 2", status="completed", result="Result 2")
        ]
    )
    response = refiner(context)
    
    assert response is not None
    assert isinstance(response.text, str)
    assert len(response.text) > 0
    assert "Test objective" in response.text
    assert "Result 1" in response.text
    assert "Result 2" in response.text

def test_refiner_with_code_project():
    context = AgentContext(
        objective="Create a Python script that calculates fibonacci numbers",
        tasks=[
            Task(id="1", description="Write fibonacci function", status="completed", result="def fibonacci(n):\n    if n <= 1:\n        return n\n    else:\n        return fibonacci(n-1) + fibonacci(n-2)"),
            Task(id="2", description="Write main function", status="completed", result="def main():\n    n = 10\n    print(f'The {n}th Fibonacci number is: {fibonacci(n)}')")
        ]
    )
    response = refiner(context)
    
    assert response is not None
    assert isinstance(response.text, str)
    assert len(response.text) > 0
    assert "Project Name:" in response.text
    assert "" in response.text
    assert "Filename:" in response.text
    assert "```python" in response.text