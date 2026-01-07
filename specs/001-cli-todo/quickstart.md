# Quickstart Guide: CLI Todo Application

## Prerequisites
- Python 3.13+
- UV package manager or pip

## Setup
1. Clone the repository
2. Install dependencies: `uv sync` or `pip install -r requirements.txt` or `pip install -e .`
3. Run the application: `python -m src.cli.main`

## Usage
1. Launch the application: `python -m src/cli/main.py`
2. Use arrow keys to navigate between menu options and tasks
3. Press Enter to select an option or confirm an action
4. Follow the interactive prompts for each operation
5. Tasks are displayed with visual indicators (✓ for completed, ○ for pending) and color coding
6. For large task lists (>20 tasks), a note will appear suggesting filtering options

## Available Operations
- **Add Task**: Create a new task with title and optional description
- **View Tasks**: Display all tasks with their status (completed/incomplete) using arrow-key navigation
- **Update Task**: Select and modify an existing task by navigating with arrows and pressing Enter
- **Delete Task**: Select and remove a task using arrow-key navigation
- **Mark Complete**: Toggle completion status of a task using arrow-key navigation
- **Exit**: Quit the application

## Interactive Features
- Arrow-key navigation for all selections
- Color-coded display (green for completed tasks, red for pending tasks)
- Icons (✓ for completed, ○ for pending) for visual distinction
- Pagination for large task lists (more than 20 tasks)
- Formatted error messages with color coding
- Confirmation prompts for destructive operations (delete)

## Task Management Features
- Auto-generated sequential task IDs
- Task completion toggling
- Task descriptions (optional, max 500 characters)
- Title validation (non-empty required)
- Description validation (max 500 characters)

## Testing
- Run all tests: `pytest`
- Run unit tests: `pytest tests/unit/`
- Run integration tests: `pytest tests/integration/`
- Run contract tests: `pytest tests/contract/`
- Run performance tests: `pytest tests/performance/`
- Run validation tests: `pytest tests/validation/`

## Development
- All code follows TDD principles with comprehensive test coverage
- In-memory storage only (no persistent data)
- No network communication during runtime
- Python 3.13+ with dataclasses and type hints