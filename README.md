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

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/calvinmagezi/praxis-ai-core.git
   cd praxis-ai-core
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install required packages:

   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

Run Praxis AI from the project root:

```
python main.py
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
├── requirements.txt       # Project dependencies
├── workspace_manager.py   # Workspace management functionality
└── README.md
```

## Core Components

### Workspace Manager

The `WorkspaceManager` class handles the creation, selection, and management of workspaces. It provides persistence for workspace data and ensures that all operations are performed in the context of the current workspace.

### Orchestrator

The orchestrator breaks down complex objectives into manageable sub-tasks. It considers the current workspace context and previous results to generate appropriate sub-tasks.

### Sub-agent

Sub-agents are specialized components that execute specific tasks. They receive instructions from the orchestrator and perform the required actions, considering the current workspace context.

### Refiner

The refiner consolidates the results from sub-agents and provides a cohesive final output. It ensures that the overall objective is met and that the output is consistent with the current workspace context.

## Command-line Interface

The CLI provides a rich, interactive interface for users to interact with Praxis AI. It uses the `rich` library to display colorful, formatted output and intuitive prompts for user input.

## Error Handling and Logging

Praxis AI implements comprehensive error handling throughout the application. Errors are caught, logged, and presented to the user in a friendly manner. The logging system tracks all operations and aids in debugging and troubleshooting.

## Contributing

Contributions to Praxis AI are welcome! To contribute:

1. Fork the repository
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Special Acknowledgments

- The [Ell framework](https://docs.ell.so/index.html) for simplifying language model interactions and providing a solid foundation for AI-assisted task completion.
- The [Maestro project](https://github.com/Doriandarko/maestro) for inspiring the concept of AI-driven task management and problem-solving.
- All contributors and users of Praxis AI who help improve and expand its capabilities.

## Future Developments

Praxis AI is an ongoing project with plans for continuous improvement and expansion. Future developments may include:

- Integration with more AI models and services
- Enhanced web search and information retrieval capabilities
- A web-based user interface for broader accessibility
- Collaborative features for team-based problem-solving
- Expanded tool integrations for more diverse task handling

Stay tuned for updates and feel free to contribute ideas or code to shape the future of Praxis AI!
