# Changelog

All notable changes to Praxis AI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
