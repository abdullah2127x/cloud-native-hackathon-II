# API Contracts: CLI Todo Application

## Task Service Interface

### Methods

#### `add_task(title: str, description: str = None) -> int`
- **Purpose**: Add a new task to the task list
- **Parameters**:
  - title (str): Task title (required, non-empty)
  - description (str, optional): Task description (max 500 chars)
- **Returns**: int - The auto-generated ID of the new task
- **Raises**: ValueError if title is empty

#### `get_all_tasks() -> List[Dict]`
- **Purpose**: Retrieve all tasks in the task list
- **Returns**: List of task dictionaries with id, title, description, completed fields
- **Note**: Returns empty list if no tasks exist

#### `get_task_by_id(task_id: int) -> Optional[Dict]`
- **Purpose**: Retrieve a specific task by its ID
- **Parameters**: task_id (int): ID of task to retrieve
- **Returns**: Dict of task details if found, None if not found

#### `update_task(task_id: int, title: str = None, description: str = None) -> bool`
- **Purpose**: Update an existing task's details
- **Parameters**:
  - task_id (int): ID of task to update
  - title (str, optional): New title if provided
  - description (str, optional): New description if provided
- **Returns**: bool - True if update successful, False if task not found

#### `delete_task(task_id: int) -> bool`
- **Purpose**: Remove a task from the task list
- **Parameters**: task_id (int): ID of task to delete
- **Returns**: bool - True if deletion successful, False if task not found

#### `toggle_task_completion(task_id: int) -> bool`
- **Purpose**: Toggle the completion status of a task
- **Parameters**: task_id (int): ID of task to toggle
- **Returns**: bool - True if toggle successful, False if task not found

#### `get_task_count() -> int`
- **Purpose**: Get the total number of tasks in the list
- **Returns**: int - Total count of tasks

#### `get_completed_tasks() -> List[Dict]`
- **Purpose**: Retrieve all completed tasks
- **Returns**: List of completed task dictionaries

#### `get_pending_tasks() -> List[Dict]`
- **Purpose**: Retrieve all pending tasks
- **Returns**: List of pending task dictionaries