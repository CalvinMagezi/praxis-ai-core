# Praxis AI

Praxis AI is an advanced, scalable AI assistant that leverages an orchestrator, sub-agent, and refiner model to break down and complete complex tasks. Inspired by the Maestro project, Praxis AI takes task management and AI-assisted problem-solving to the next level with its workspace-centric approach and enhanced user interaction.

Version: 0.1.0
Author: Calvin Magezi (GitHub: [@calvinmagezi](https://github.com/calvinmagezi))

## Features

- **Workspace Management**: Create, switch between, and manage multiple workspaces for organized project handling.
- **Orchestrator**: Breaks down complex objectives into manageable sub-tasks.
- **Sub-agents**: Execute specific tasks with specialized knowledge.
- **Refiner**: Consolidates and improves results from sub-agents.
- **Modular Architecture**: Easily expand and integrate new tools and functionalities.
- **Rich Command-line Interface**: User-friendly CLI with colorful, informative output.
- **API Interface**: FastAPI-based API for programmatic access to Praxis AI capabilities.
- **Logging System**: Comprehensive logging for tracking operations and debugging.
- **Persistent Storage**: Save and load workspace data between sessions.
- **Error Handling**: Robust error handling throughout the application.
- **Pip-installable Package**: Easy installation and usage as a Python package.
- **Chat History**: Store and retrieve conversation history within workspaces.
- **Workspace-Aware File Operations**: All file operations are performed within the context of the current workspace.
- **API Key Management**: Securely manage and use API keys for various services.

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

3. Install Praxis AI:

   ```
   pip install -e .
   ```

   This will install Praxis AI in editable mode, allowing you to make changes to the code and immediately see the effects.

4. Set up environment variables:
   Create a `.env` file in the project root and add your API keys:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

   Alternatively, you can set these environment variables in your shell:

   ```
   export OPENAI_API_KEY=your_openai_api_key_here
   export ANTHROPIC_API_KEY=your_anthropic_api_key_here
   export TAVILY_API_KEY=your_tavily_api_key_here
   export GROQ_API_KEY=your_groq_api_key_here
   ```

## Usage

After installation, you can use Praxis AI through its command-line interface:

1. List available workspaces:

   ```
   praxis list
   ```

2. Create a new workspace:

   ```
   praxis enter
   ```

   If no workspaces exist, you'll be prompted to create one.

3. Enter an existing workspace:

   ```
   praxis enter "Workspace Name"
   ```

4. Start a chat session within a workspace:

   Once you've entered a workspace, you'll be in chat mode. You can have a conversation with Praxis or start an objective:

   ```
   objective: Create a Python script that calculates prime numbers
   ```

5. View conversation history:

   ```
   praxis history --workspace "Workspace Name"
   ```

   If no workspace is specified, it will show the history for the current workspace.

6. Exit a workspace:

   Type 'exit' when in chat mode to leave the workspace.

## API Usage

To use the Praxis AI API:

1. Start the FastAPI server:

   ```
   uvicorn praxis_ai.interfaces.api:app --reload
   ```

2. Send a POST request to `http://localhost:8000/process_objective` with a JSON body containing the objective:

   ```json
   {
     "objective": "Create a marketing plan for a new product launch"
   }
   ```

## Project Structure

```
praxis_ai/
├── praxis_ai/
│   ├── __init__.py
│   ├── cli.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── models.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── orchestrator.py
│   │   ├── sub_agent.py
│   │   └── refiner.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── file_operations.py
│   │   └── web_search.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logging.py
│   │   └── helpers.py
│   ├── interfaces/
│   │   ├── __init__.py
│   │   └── api.py
│   └── workspace_manager.py
├── tests/
│   ├── __init__.py
│   ├── test_orchestrator.py
│   ├── test_sub_agent.py
│   └── test_refiner.py
├── setup.py
├── requirements.txt
├── README.md
├── LICENSE
└── .env
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

## API Interface

The FastAPI-based API allows for programmatic access to Praxis AI's capabilities, enabling integration with other applications and services.

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

## Acknowledgments

- OpenAI for providing the GPT models that power Praxis AI's language understanding and generation capabilities.
- The Ell framework for simplifying language model interactions and providing a solid foundation for AI-assisted task completion.
- The Maestro project for inspiring the concept of AI-driven task management and problem-solving.
- All contributors and users of Praxis AI who help improve and expand its capabilities.

## Troubleshooting

If you encounter any issues:

1. Ensure all required environment variables (API keys) are set correctly.
2. Check that you're using a compatible Python version (3.7+).
3. Make sure all dependencies are installed correctly (`pip install -r requirements.txt`).
4. If you encounter any "module not found" errors, try reinstalling the package (`pip install -e .`).

For more help, please open an issue on the GitHub repository.

## Future Developments

Praxis AI is an ongoing project with plans for continuous improvement and expansion. Future developments may include:

- Integration with more AI models and services
- Enhanced web search and information retrieval capabilities
- A web-based user interface for broader accessibility
- Collaborative features for team-based problem-solving
- Expanded tool integrations for more diverse task handling

Stay tuned for updates and feel free to contribute ideas or code to shape the future of Praxis AI!
