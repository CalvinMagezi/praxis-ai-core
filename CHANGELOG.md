# Changelog

All notable changes to Praxis AI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

## [0.1.0] - 2024-09-24

### ⚠️ BREAKING CHANGES

This release contains significant breaking changes. Please review carefully before upgrading.

### Added

- Workspace-aware functionality
  - All operations are now performed within the context of the current workspace
  - File operations (read/write) are workspace-specific
- Chat history feature
  - Conversations are now stored as individual chat files within each workspace
  - New `praxis history` command to view past conversations
- API key management
  - Automatic checking for OpenAI API key on startup
  - Prompt for API key input if not found in environment variables
- Enhanced CLI commands
  - `praxis enter` command now supports entering workspaces directly
  - Added `--workspace` option to various commands for specifying workspaces
- Persistent chat sessions
  - Chat sessions are automatically saved when exiting a workspace
  - Chat titles are derived from the first few words of the conversation

### Changed

- Restructured project layout for better modularity
  - Moved core components into separate modules
  - Reorganized utility functions and tools
- Updated `WorkspaceManager` class
  - Added methods for managing chat history and logs
  - Improved error handling and workspace selection
- Modified `cli.py` to support new workspace-aware and chat features
  - Updated main CLI group to include API key checking
  - Refactored command functions to work with new workspace structure
- Revised `file_operations.py` to be workspace-aware
  - All file operations now take workspace context into account
- Updated `orchestrator`, `sub_agent`, and `refiner` to work within workspace context
- Modified API interface to support workspace-aware operations

### Removed

- Removed global state management in favor of workspace-specific state
- Eliminated deprecated utility functions that were not workspace-aware

### Fixed

- Resolved issues with concurrent access to workspaces
- Fixed bugs related to file path handling in different operating systems
- Addressed race conditions in chat history saving

## [0.0.1] - 2024-09-23

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
