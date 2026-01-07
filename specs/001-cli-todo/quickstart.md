# Quickstart Guide: CLI Todo Application

## Prerequisites
- Python 3.13+
- UV package manager

## Setup
1. Clone the repository
2. Install dependencies: `uv sync` or `pip install -r requirements.txt`
3. Run the application: `python -m src.cli.main`

## Usage
1. Launch the application: `python -m src.cli.main`
2. Use arrow keys to navigate between options and tasks
3. Press Enter to select an option or confirm an action
4. Follow the interactive prompts for each operation
5. For large task lists, use pagination controls to navigate through pages

## Available Operations
- **Add Task**: Create a new task with title and optional description
- **View Tasks**: Display all tasks with their status (completed/incomplete) using arrow-key navigation
- **Update Task**: Select and modify an existing task by navigating with arrows and pressing Enter
- **Delete Task**: Select and remove a task using arrow-key navigation
- **Mark Complete**: Toggle completion status of a task using arrow-key navigation

## Interactive Features
- Arrow-key navigation for all selections
- Color-coded display for completed vs pending tasks
- Icons and formatting for visual distinction
- Pagination for large task lists (more than 20 tasks)
- Error messages with formatting

## Testing
- Run all tests: `pytest`
- Run unit tests: `pytest tests/unit/`
- Run integration tests: `pytest tests/integration/`
- Run contract tests: `pytest tests/contract/`