# Praxis AI

Praxis AI is an advanced, scalable AI assistant that leverages an orchestrator, sub-agent, and refiner model to break down and complete complex tasks. Inspired by the Maestro project, Praxis AI takes task management and AI-assisted problem-solving to the next level with its workspace-centric approach and enhanced user interaction.

Version: 0.1.8
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
- **Advanced File Handling**: Create, read, copy, move, and delete various file types including PDFs, Word documents, and Markdown files within workspaces.
- **Conversation History Management**: Maintain and utilize conversation history for context-aware interactions across sessions.
- **Chat History**: Store and retrieve conversation history within workspaces.
- **Workspace-Aware File Operations**: All file operations are performed within the context of the current workspace.
- **API Key Management**: Securely manage and use API keys for various services.
- **Chat-Based Interaction**: Intuitive chat interface for all Praxis AI interactions.
- **Advanced Tool Execution**: Improved tool calling mechanism using the Ell framework.
- **Enhanced Web Search**: Integrated web search functionality using the Tavily API, with caching for faster repeated searches and rich formatting of results.
- **Google Calendar Integration**: Schedule meetings and manage calendar events directly through Praxis AI.
- **Improved File Type Detection**: Better handling of various file types using the python-magic library.

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

4. Install additional dependencies:

   ```
   pip install reportlab python-docx markdown tavily-python google-auth-oauthlib google-api-python-client python-magic
   ```

5. Set up environment variables:
   Create a `.env` file in the project root and add your API keys:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
   ENABLE_CALENDAR=true
   ```

   Alternatively, you can set these environment variables in your shell.

6. Set up Google Calendar credentials:
   - Follow the steps in the "Google Calendar Setup" section below to obtain your `credentials.json` file.
   - Place the `credentials.json` file in the root of your project folder.

## Google Calendar Setup

To use the Google Calendar integration:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the Google Calendar API for your project.
4. Create credentials (OAuth client ID) for a Desktop application.
5. Download the credentials and save them as `credentials.json` in your project root.
6. Update the `GOOGLE_CALENDAR_CREDENTIALS_FILE` in `config/settings.py` to point to this file.

## Usage

After installation, you can use Praxis AI through its command-line interface:

1. Start Praxis AI:

   ```
   praxis
   ```

2. Once Praxis AI starts, you'll be in a chat interface. You can interact with Praxis using natural language. For example:

   - To create a new workspace: "Create a new workspace called Projects for managing my projects"
   - To list workspaces: "List all my workspaces"
   - To enter a workspace: "Enter the Projects workspace"
   - To start an objective: "I want to create a Python script that calculates prime numbers"
   - To create a PDF: "Create a PDF file named 'report.pdf' with the content 'This is a test report.'"
   - To read a Word document: "Read the contents of the file 'meeting_notes.docx'"
   - To create a Markdown file: "Create a Markdown file named 'todo.md' with a list of tasks"
   - To copy a file: "Copy the file 'report.pdf' to 'backup_report.pdf'"
   - To move a file: "Move the file 'old_notes.txt' to the 'archive' folder"
   - To delete a file: "Delete the file 'temp.txt'"
   - To list files in a directory: "List all files in the 'documents' folder"
   - To perform a web search: "Search for the latest developments in quantum computing"
   - To schedule a meeting: "Schedule a meeting with John Doe about project updates tomorrow at 2 PM for 1 hour"
   - To list upcoming meetings: "What are my upcoming meetings for this week?"

3. Praxis will guide you through the process, using various tools to accomplish tasks as needed.

4. Praxis AI now maintains conversation history. You can ask about previous interactions within the same workspace.

5. To exit Praxis AI, simply type 'exit' in the chat interface.

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
│   │   ├── refiner.py
│   │   └── chat.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── file_operations.py
│   │   ├── web_search.py
│   │   └── calendar_tools.py
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
├── CHANGELOG.md
├── LICENSE
├── .env
└── credentials.json
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

### File Operations

The `file_operations.py` module contains tools for creating, reading, copying, moving, and deleting various file types, including PDFs, Word documents, and Markdown files. These operations are workspace-aware, ensuring that files are managed within the context of the current workspace. The module now includes improved file type detection using the python-magic library.

### Web Search

The `web_search.py` module provides enhanced web search capabilities using the Tavily API. It includes features such as result caching, rich formatting of search results, and automatic retries for improved reliability.

### Calendar Tools

The `calendar_tools.py` module integrates with Google Calendar, allowing Praxis AI to schedule meetings, list upcoming events, and manage calendar-related tasks.

### Chat Interface

The chat interface provides a natural language interaction point for users to communicate with Praxis AI. It interprets user inputs, manages tool executions, and presents results in a conversational manner.

## Command-line Interface

The CLI now provides a chat-based interface for interacting with Praxis AI. It uses the `rich` library to display colorful, formatted output and intuitive prompts for user input.

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
- The reportlab, python-docx, and markdown libraries for enabling advanced file handling capabilities.
- Tavily for providing the API that powers Praxis AI's web search capabilities.
- Google for the Calendar API that enables Praxis AI's scheduling capabilities.
- The python-magic library for improved file type detection.

## Troubleshooting

If you encounter any issues:

1. Ensure all required environment variables (API keys) are set correctly, including the Tavily API key for web search functionality and the path to your Google Calendar credentials.
2. Check that you're using a compatible Python version (3.7+).
3. Make sure all dependencies are installed correctly (`pip install -r requirements.txt`).
4. If you encounter any "module not found" errors, try reinstalling the package (`pip install -e .`).
5. If you encounter issues with tool execution or unexpected responses, check the debug output in the console for more information about tool calls and their results.
6. If you encounter issues with file creation, reading, or manipulation, ensure that you have the necessary permissions in the workspace directory and that the required libraries (reportlab, python-docx, markdown, python-magic) are correctly installed.
7. If web searches are not working, verify that your Tavily API key is correct and that you have an active internet connection.
8. If search results are not displaying correctly, ensure that your terminal supports rich text formatting.
9. For Google Calendar integration issues, ensure that you've completed the Google Calendar setup process correctly and that your `credentials.json` file is in the correct location.

For more help, please open an issue on the GitHub repository.

## Future Developments

Praxis AI is an ongoing project with plans for continuous improvement and expansion. Future developments may include:

- Integration with more AI models and services
- Further enhancements to web search and information retrieval capabilities
- A web-based user interface for broader accessibility
- Collaborative features for team-based problem-solving
- Expanded tool integrations for more diverse task handling
- Further enhancements to file handling capabilities, including support for more file formats and advanced operations like file merging and splitting.
- Enhanced calendar integration with support for more complex scheduling scenarios and multi-calendar management.
- Improved natural language processing for more intuitive file and workspace management commands.

Stay tuned for updates and feel free to contribute ideas or code to shape the future of Praxis AI!
