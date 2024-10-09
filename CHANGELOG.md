# Changelog

All notable changes to Praxis AI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2024-10-09

### Added

- Implemented Realtime API functionality
  - New WebSocket-based server for real-time communication
  - Support for audio input and output
  - Integration with OpenAI's GPT-4 model
  - Text transcription of audio inputs and outputs
  - Conversation history management within WebSocket sessions
  - Moderation of content for appropriate responses
- New frontend application for interacting with the Realtime API
  - Audio recording and playback capabilities
  - Real-time text and audio message display
- Enhanced error handling and reconnection logic for WebSocket connections
- New directory structure for Realtime API implementation:
  - `praxis_ai/interfaces/realtime-api/backend/server.js`
  - `praxis_ai/interfaces/realtime-api/src/App.js`
  - `praxis_ai/interfaces/realtime-api/src/App.css`

### Changed

- Updated project structure to include the new Realtime API implementation
- Modified README to include information about the Realtime API feature

### Improved

- Real-time interaction capabilities of Praxis AI
- Multi-modal communication support (text and audio)
- Robustness of WebSocket connections with error handling and reconnection logic

## [0.1.8] - 2024-10-01

### Added

- Enhanced file operation tools with new functionalities:
  - `copy_file_tool`: Copies a file within the workspace.
  - `move_file_tool`: Moves a file within the workspace.
  - `delete_file_tool`: Deletes a file from the workspace.
  - `list_files_tool`: Lists files in a directory within the workspace.
- Improved file type detection using the `python-magic` library.
- Better handling of binary files in read operations.

### Changed

- Updated `file_operations.py` with new and improved file operation functions.
- Modified `core/chat.py` to include new file operation tools and update system message.
- Updated `cli.py` to import and utilize the new file operation tools.

### Improved

- More robust and flexible file operations within workspaces.
- Enhanced error handling and logging for file operations.
- Better integration of file operations into the chat interface.

## [0.1.7] - 2024-09-30

### Added

- Enhanced calendar tools with new functionalities:
  - `get_user_timezone`: Retrieves the user's timezone.
  - `update_meeting`: Updates an existing meeting.
  - `delete_meeting`: Deletes a meeting.
  - `find_free_time`: Finds available time slots.
- Optional calendar functionality controlled by the `ENABLE_CALENDAR` setting.
- Prompts for Google Calendar credentials if needed.

### Changed

- Updated `calendar_tools.py` with enhanced functions and optional calendar support.
- Modified `core/chat.py` to include new calendar tools and handle optional calendar functionality.
- Updated `cli.py` to inform the user about calendar functionality and prompt for credentials if necessary.

### Improved

- More robust and flexible calendar integration.
- Better user experience with optional calendar features and credential prompting.

## [0.1.6] - 2024-09-29

### Added

- Google Calendar integration
- New `calendar_tools.py` module for interacting with Google Calendar API
- `schedule_meeting` tool for creating calendar events
- `list_upcoming_meetings` tool for retrieving upcoming events
- Google Calendar setup instructions in README
- New configuration for Google Calendar credentials in settings

### Changed

- Updated `core/chat.py` to include new calendar tools
- Modified CLI to handle and display calendar-related results
- Enhanced API key checking to include Google Calendar credentials
- Updated `requirements.txt` to include Google Calendar API dependencies

### Improved

- More comprehensive scheduling capabilities within Praxis AI
- Better integration of calendar management into the chat interface

## [0.1.5] - 2024-09-28

### Added

- Enhanced web search functionality using Tavily API
- Caching for faster repeated searches using @lru_cache
- Rich formatting for better display of search results
- Summary of search results in addition to detailed results
- Improved error handling with automatic retries for web searches
- New configuration for Tavily API key in settings

### Changed

- Updated web_search tool to use Tavily API and provide more detailed results
- Modified CLI to handle and display formatted web search results
- Improved API key checking to include both OpenAI and Tavily keys
- Enhanced execute_tool function in CLI to handle web search results differently

### Improved

- Better integration of web search results into the chat interface
- More informative and visually appealing display of search results
- Faster response times for repeated or similar web searches due to caching

## [0.1.4] - 2024-09-27

### Added

- New file handling capabilities:
  - Create and read PDF files
  - Create and read Word documents
  - Create and read Markdown files
- Conversation history management within workspaces
- New tools for file operations in `file_operations.py`
- Updated `chat` function to handle new file operations and maintain conversation history

### Changed

- ⚠️ BREAKING CHANGE: Replaced PyPDF library with reportlab for PDF creation
- Updated `requirements.txt` to include new dependencies: reportlab, python-docx, markdown
- Modified `cli.py` to handle new file operations and conversation history
- Enhanced error handling in file operations

### Fixed

- Resolved issue with PDF creation failing due to incompatible PyPDF library

## [0.1.3] - 2024-09-27

### Added

- Improved chat-based interface for all Praxis AI interactions
- Enhanced tool execution framework using Ell's tool calling mechanism
- New `execute_tool` function for more robust tool handling
- Debug output for tool calls to aid in troubleshooting

### Changed

- Refactored `cli.py` to use a chat-based interaction model
- Updated `chat` function in `core/chat.py` to better handle tool calls and results
- Modified `WorkspaceManager` to support the new chat-based workflow
- Improved error handling and reporting in tool execution

### Fixed

- Resolved issues with tool execution not being reflected in Praxis's responses
- Fixed inconsistencies in workspace creation and listing

## [0.1.2] - 2024-09-25

### Added

- New workspace initialization helper function
  - Automatically creates a predefined folder structure for new workspaces
  - Sets up Chat, Studio, Automations, Builder, and Memory folders with respective subfolders
- Improved visual feedback during workspace initialization
  - Added progress indicators with spinning animations for each main folder setup
- New root-level CLI structure
  - `praxis` command now displays a list of available commands
  - Added `create` command for creating and initializing a new workspace
  - Added `delete` command for removing workspaces with a warning
- Workspace-specific CLI with `chat`, `obj`/`objective`, `history`, and `exit` commands
- Short version `obj` as an alias for `objective` command

### Changed

- Enhanced CLI feedback during task execution
  - Replaced generic "thinking" messages with more contextual status updates
  - Now provides specific information about current actions (e.g., "Breaking down tasks", "Evaluating progress")
- Updated `create_new_workspace` function to use the new initialization helper
- Modified `handle_objective` function to give more detailed progress information
- Restructured CLI flow for better user experience
  - Root-level commands for workspace management
  - Workspace-specific commands accessible after entering a workspace
- `enter` command now leads to a workspace-specific CLI
- `history` command is now only available within a workspace context

### Improved

- User experience during workspace creation and task execution
- Clarity of CLI output with more specific status messages
- Clearer separation between workspace management and workspace-specific operations
- More intuitive command structure and flow
- Enhanced safety with confirmation step for workspace deletion

### Removed

- Removed direct access to workspace-specific functions from root level

## [0.1.1] - 2024-09-24

### Added

- New `chat.py` module in the core directory
  - Implements an Ell-based chat function for more sophisticated language model interactions
  - Utilizes the `@ell.complex` decorator for advanced functionality
- Workspace-aware chat functionality
  - Chat now considers the full conversation history within the current workspace
  - Improved context retention across chat sessions
- New `CHAT_MODEL` setting in `config/settings.py`
  - Allows for easy configuration of the language model used for chat interactions

### Changed

- Refactored `cli.py` to use the new Ell-based chat function
  - `start_chat_mode` now utilizes the chat function from `core/chat.py`
  - Improved integration with `WorkspaceManager` for conversation history management
- Enhanced conversation history handling
  - Chat sessions now maintain and utilize the full conversation context
  - Improved persistence of chat sessions across workspace interactions

### Improved

- Better scalability for chat functionality
  - Chat logic is now isolated in its own module, allowing for easier future enhancements
- More consistent user experience across different Praxis AI components
  - Chat now uses similar Ell-based architecture as orchestrator, sub-agent, and refiner

## [0.1.0] - 2024-09-23

### Added

- Initial release of Praxis AI
- Basic workspace management functionality
- Orchestrator for breaking down tasks
- Sub-agents for executing specific tasks
- Refiner for consolidating results
- Simple command-line interface
- Basic error handling and logging system

## [Unreleased]

### Planned

- Integration with additional AI models and services
- Enhanced web search capabilities
- Web-based user interface
- Collaborative features for team-based problem-solving
- Expanded tool integrations
