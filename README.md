# CLI Todo Application

A feature-rich command-line interface todo application with in-memory storage, built with Python.

## Features

- **Interactive CLI**: User-friendly interface with arrow-key navigation
- **Task Management**: Add, view, update, delete, and mark tasks as complete/incomplete
- **Visual Design**: Color-coded output with icons and formatted tables using rich
- **Validation**: Comprehensive input validation and error handling
- **In-Memory Storage**: Fast operations with no persistent storage
- **TDD Approach**: Fully tested with unit, integration, and contract tests

## Requirements

- Python 3.13+
- UV package manager or pip

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   or
   ```bash
   pip install -e .
   ```

## Usage

Run the application:
```bash
python -m src.cli.main
```

### Available Operations

- **Add Task**: Create a new task with title and optional description
- **View Tasks**: Display all tasks with their status (completed/incomplete) using formatted tables
- **Update Task**: Modify an existing task's title or description
- **Delete Task**: Remove a task with confirmation prompt
- **Mark Task Complete/Incomplete**: Toggle completion status with visual indicators
- **Exit**: Quit the application

### Visual Elements

- ✓ Green checkmark for completed tasks
- ○ Red circle for pending tasks
- Color-coded status indicators
- Formatted tables for task display
- Styled panels and messages

## Project Structure

```
src/
├── models/           # Data models (Task, TaskList)
├── services/         # Business logic (TaskService)
├── cli/              # Command-line interface
└── lib/              # Utilities (validators)
tests/
├── unit/             # Unit tests
├── integration/      # Integration tests
├── contract/         # Contract tests
└── validation/       # Validation tests
```

## Testing

Run all tests:
```bash
pytest
```

Run specific test suites:
```bash
pytest tests/unit/        # Unit tests
pytest tests/integration/ # Integration tests
pytest tests/contract/    # Contract tests
pytest tests/validation/  # Validation tests
```

## Architecture

- **Model Layer**: Task and TaskList entities with validation
- **Service Layer**: TaskService with business logic and validation
- **CLI Layer**: Interactive command-line interface with rich formatting
- **Validation Layer**: Comprehensive input validation utilities

## Performance

- Handles 100+ tasks in memory
- Operations complete in under 5 seconds
- Memory usage optimized for in-memory storage

## Compliance

- TDD implementation with comprehensive test coverage
- No network communication during runtime
- In-memory only storage (no file I/O or databases)
- Python 3.13+ with proper error handling and type hints