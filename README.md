<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://praxis-app.online/logo.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://praxis-app.online/logo.svg">
  <img alt="ell logo that inverts based on color scheme" src="https://praxis-app.online/logo.svg">
</picture>

# Praxis AI

Praxis AI is an advanced, scalable AI assistant that leverages an orchestrator, sub-agent, and refiner model to break down and complete complex tasks. Inspired by the Maestro project, Praxis AI takes task management and AI-assisted problem-solving to the next level with its workspace-centric approach and enhanced user interaction.

Version: 0.0.1
Author: Calvin Magezi (GitHub: [@calvinmagezi](https://github.com/calvinmagezi))

[Try Praxis In The Cloud](https://praxis-app.online/), built by [Magezi Tech Solutions](https://mts-africa.tech/)

## Features

- **Workspace Management**: Create, switch between, and manage multiple workspaces for organized project handling.
- **Orchestrator**: Breaks down complex objectives into manageable sub-tasks.
- **Sub-agents**: Execute specific tasks with specialized knowledge.
- **Refiner**: Consolidates and improves results from sub-agents.
- **Modular Architecture**: Easily expand and integrate new tools and functionalities.
- **Rich Command-line Interface**: User-friendly CLI with colorful, informative output.
- **Logging System**: Comprehensive logging for tracking operations and debugging.
- **Persistent Storage**: Save and load workspace data between sessions.
- **Error Handling**: Robust error handling throughout the application.

## Requirements

- Python 3.7.1 or higher

## Installation

### Option 1: Install via pip (Recommended for users)

You can install Praxis AI directly from PyPI using pip:

```
pip install praxis-ai
```

### Option 2: Install using Poetry (Recommended for developers)

1. Ensure you have Poetry installed. If not, install it by following the instructions at [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation)

2. Clone the repository:

   ```
   git clone https://github.com/calvinmagezi/praxis-ai-core.git
   cd praxis-ai-core
   ```

3. Install dependencies using Poetry:

   ```
   poetry install
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### If installed via pip:

Run Praxis AI from anywhere in your terminal:

```
praxis-ai
```

### If installed using Poetry:

Run Praxis AI using Poetry:

```
poetry run praxis-ai
```

Alternatively, you can activate the Poetry virtual environment and then run the app:

```
poetry shell
praxis-ai
```

Upon launching, you'll be greeted with a welcome message and a list of available commands. Here's what you can do:

- **Create a new workspace**: Organize your projects in separate workspaces.
- **Switch workspaces**: Move between different project contexts.
- **Delete workspaces**: Remove workspaces you no longer need.
- **List workspaces**: View all available workspaces.
- **Enter an objective**: Provide a task for Praxis AI to work on.
- **Quit**: Exit the application.

Follow the on-screen prompts to interact with Praxis AI and complete your objectives.

## Project Structure

```
praxis_ai/
├── config/
│   ├── __init__.py
│   ├── settings.py        # Global configuration settings
│   └── models.py          # Pydantic models for data structures
├── core/
│   ├── __init__.py
│   ├── orchestrator.py    # Task breakdown and management
│   ├── sub_agent.py       # Specialized task execution
│   └── refiner.py         # Result consolidation and improvement
├── tools/
│   ├── __init__.py
│   ├── file_operations.py # File and folder management utilities
│   └── web_search.py      # Web search functionality (placeholder)
├── utils/
│   ├── __init__.py
│   ├── logging.py         # Logging configuration and utilities
│   └── helpers.py         # General helper functions
├── interfaces/
│   ├── __init__.py
│   ├── cli.py             # Command-line interface
│   └── api.py             # API interface (placeholder for future use)
├── data/
│   └── .gitkeep           # Directory for storing workspace data
├── tests/
│   ├── __init__.py
│   ├── test_orchestrator.py
│   ├── test_sub_agent.py
│   └── test_refiner.py
├── main.py                # Entry point of the application
├── pyproject.toml         # Poetry configuration and project metadata
├── setup.py               # Setuptools configuration for pip compatibility
└── README.md
```

## Core Components

[The rest of the README content remains unchanged]
