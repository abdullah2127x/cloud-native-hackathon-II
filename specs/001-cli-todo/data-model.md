# Data Model: CLI Todo Application

## Task Entity

### Fields
- **id**: Integer (auto-generated sequential number, primary identifier)
- **title**: String (required, validated to not be empty)
- **description**: String (optional, max 500 characters)
- **completed**: Boolean (default: false)

### Validation Rules
- Title must not be empty or whitespace-only (prompt user to re-enter if empty)
- Description, if provided, must not exceed 500 characters
- ID must be unique within the application session
- ID must be auto-generated as sequential numbers (1, 2, 3, etc.)

### State Transitions
- `pending` → `completed`: When user marks task as complete
- `completed` → `pending`: When user marks task as incomplete

### Relationships
- Task List contains multiple Task entities
- Each Task belongs to one Task List (in-memory collection)

## Task List Entity

### Fields
- **tasks**: List of Task entities (in-memory storage)
- **next_id**: Integer (counter for next auto-generated ID)

### Operations
- Add Task: Append to tasks list, assign next available ID
- Remove Task: Remove by ID, validate existence before removal
- Update Task: Find by ID, update specified fields
- Mark Complete: Find by ID, toggle completion status
- List Tasks: Return all tasks in the collection