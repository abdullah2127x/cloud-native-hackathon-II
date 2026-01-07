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
2. Use arrow keys to navigate between options
3. Press Enter to select an option
4. Follow the interactive prompts for each operation

## Available Operations
- **Add Task**: Create a new task with title and optional description
- **View Tasks**: Display all tasks with their status (completed/incomplete)
- **Update Task**: Modify an existing task by ID
- **Delete Task**: Remove a task by ID
- **Mark Complete**: Toggle completion status of a task by ID

## Testing
- Run all tests: `pytest`
- Run unit tests: `pytest tests/unit/`
- Run integration tests: `pytest tests/integration/`