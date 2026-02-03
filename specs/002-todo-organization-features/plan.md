# Implementation Plan: Todo Organization & Usability Features

**Branch**: `002-todo-organization-features` | **Date**: 2026-01-23 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-todo-organization-features/spec.md`
**Constitution Version**: 2.2.1

## Summary

Extend the existing task management system with organizational features: task priorities (High/Medium/Low/None), multi-tag categorization, keyword search, advanced filtering (status/priority/tags), and customizable sorting. All features maintain user isolation, work with existing authentication, and follow established patterns from Phase 1.

---

## Technical Context

**Frontend**:
- **Framework**: Next.js 16 (App Router) - existing
- **Language**: TypeScript (strict mode) - existing
- **Styling**: Tailwind CSS + shadcn/ui - existing
- **Form Management**: React Hook Form + Zod resolver - existing
- **Validation**: Zod schemas - existing
- **Authentication**: Better Auth (JWT tokens) - existing
- **Testing**: Jest + React Testing Library + MSW - existing
- **Coverage Target**: >=70%

**Backend**:
- **Framework**: Python FastAPI - existing
- **Language**: Python 3.13+
- **Package Manager**: uv - existing
- **ORM**: SQLModel - existing
- **Validation**: Pydantic - existing
- **Testing**: pytest + pytest-asyncio - existing
- **Coverage Target**: >=70%

**Database**:
- **Type**: PostgreSQL (Neon Serverless) - existing
- **ORM**: SQLModel with type-safe queries
- **New Tables**: `tag` (many-to-many with task via `task_tag`)

**Key Constraints**:
- User isolation: ALL queries MUST filter by `user_id`
- Performance: Search/filter within 300-500ms
- Responsiveness: Mobile-first (320px+)
- Sort preference: Persist in localStorage

---

## Constitution Check

| Principle | Requirement | Status | Evidence |
|-----------|-------------|--------|----------|
| **I. TDD** | Test-first development | PASS | Extending existing test suites, 70% coverage |
| **II. No Manual Coding** | Claude Code generates all code | PASS | Using Spec-Kit Plus workflow |
| **III. Code Quality** | Type safety, validation, error handling | PASS | TS strict, Zod/Pydantic, existing error patterns |
| **VIII. Persistent Storage** | Database required | PASS | Neon PostgreSQL with new Tag table |
| **IX. RESTful API** | REST + JSON | PASS | Extending existing FastAPI endpoints |
| **X. Security & Isolation** | User isolation, verified identity | PASS | All queries include user_id filter |
| **XI. Authentication** | JWT + Better Auth | PASS | Using existing auth infrastructure |
| **XII. Architecture** | Monorepo, separated frontend/backend | PASS | Following existing structure |
| **XIII. Performance** | <200ms API, <2s load | PASS | Debounced search, indexed queries |

**Constitution Gate**: PASSED

---

## Project Structure

### Documentation (this feature)

```text
specs/002-todo-organization-features/
├── spec.md              # Feature specification (exists)
├── plan.md              # This file
├── data-model.md        # Database schema changes
├── contracts/           # API contracts
│   ├── openapi.yaml     # OpenAPI additions
│   └── schemas.ts       # Zod schema extensions
└── tasks.md             # Task breakdown (via /sp.tasks)
```

### Source Code Changes

```text
backend/src/
├── models/
│   ├── task.py          # MODIFY: Add priority field
│   └── tag.py           # NEW: Tag model + TaskTag junction
├── schemas/
│   └── task.py          # MODIFY: Add priority, tags to schemas
├── crud/
│   ├── task.py          # MODIFY: Add filtering/sorting params
│   └── tag.py           # NEW: Tag CRUD operations
└── routers/
    ├── tasks.py         # MODIFY: Add query params for filter/sort
    └── tags.py          # NEW: Tag management endpoints

frontend/src/
├── types/
│   └── task.ts          # MODIFY: Add Priority enum, Tag type
├── lib/validations/
│   └── task.ts          # MODIFY: Add priority, tags validation
├── components/tasks/
│   ├── TaskForm.tsx     # MODIFY: Add priority selector, tag input
│   ├── TaskItem.tsx     # MODIFY: Display priority badge, tag chips
│   ├── TaskList.tsx     # MODIFY: Client-side filter/sort integration
│   ├── SearchBar.tsx    # NEW: Search input with debounce
│   ├── FilterPanel.tsx  # NEW: Status/priority/tag filters
│   ├── SortSelector.tsx # NEW: Sort dropdown
│   ├── PriorityBadge.tsx    # NEW: Visual priority indicator
│   ├── TagChip.tsx          # NEW: Clickable tag display
│   └── TagInput.tsx         # NEW: Tag autocomplete input
├── hooks/
│   ├── useTasks.ts      # MODIFY: Add filter/sort/search params
│   ├── useTags.ts       # NEW: Tag fetching/management
│   ├── useTaskFilters.ts    # NEW: Filter state management
│   └── useDebounce.ts       # NEW: Debounce utility hook
└── lib/constants/
    └── priorities.ts    # NEW: Priority enum and colors
```

---

## Data Model Changes

### Priority Enum (Backend)

```python
# backend/src/models/task.py
from enum import Enum

class Priority(str, Enum):
    """Task priority levels"""
    NONE = "none"      # Default, lowest sort order
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

# Priority sort order for database queries
PRIORITY_ORDER = {
    Priority.HIGH: 0,
    Priority.MEDIUM: 1,
    Priority.LOW: 2,
    Priority.NONE: 3,
}
```

### Extended Task Model

```python
# backend/src/models/task.py (modified)
class Task(SQLModel, table=True):
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: bool = Field(default=False)
    priority: Priority = Field(default=Priority.NONE, index=True)  # NEW
    created_at: datetime = Field(default_factory=utc_now, index=True)
    updated_at: Optional[datetime] = Field(default=None)

    # Relationship to tags (via junction table)
    tags: List["Tag"] = Relationship(back_populates="tasks", link_model="TaskTag")
```

### Tag Model (New)

```python
# backend/src/models/tag.py
class Tag(SQLModel, table=True):
    """Tag for categorizing tasks - unique per user, case-insensitive"""
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    name: str = Field(max_length=50, index=True)  # lowercase, no spaces
    created_at: datetime = Field(default_factory=utc_now)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="tags", link_model="TaskTag")

    class Config:
        # Unique constraint: (user_id, name)
        table_args = (UniqueConstraint("user_id", "name"),)


class TaskTag(SQLModel, table=True):
    """Junction table for Task-Tag many-to-many relationship"""
    task_id: str = Field(foreign_key="task.id", primary_key=True)
    tag_id: str = Field(foreign_key="tag.id", primary_key=True)
```

### Database Indexes

```sql
-- New indexes for performance
CREATE INDEX idx_task_priority ON task(user_id, priority);
CREATE INDEX idx_task_completed ON task(user_id, completed);
CREATE INDEX idx_tag_user_name ON tag(user_id, name);
```

---

## API Design

### Modified Endpoints

#### GET /api/todos - List Tasks (Enhanced)

**Query Parameters** (all optional):
| Parameter | Type | Description |
|-----------|------|-------------|
| `search` | string | Search in title + description (case-insensitive, partial match) |
| `status` | string | Filter: "all" (default), "pending", "completed" |
| `priority` | string | Filter: "all" (default), "high", "medium", "low", "none" |
| `tags` | string[] | Filter: comma-separated tag names (OR logic) |
| `no_tags` | boolean | Filter: only tasks without tags |
| `sort` | string | "priority" (default), "title", "created_at" |
| `order` | string | "asc" or "desc" (default varies by sort) |

**Response** (enhanced):
```json
{
  "tasks": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "title": "string",
      "description": "string | null",
      "completed": false,
      "priority": "high",
      "tags": ["work", "urgent"],
      "created_at": "2026-01-23T...",
      "updated_at": "2026-01-23T..."
    }
  ],
  "total": 65,
  "filtered": 18
}
```

#### POST /api/todos - Create Task (Enhanced)

**Request Body**:
```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "priority": "none | low | medium | high (default: none)",
  "tags": ["work", "urgent"] // optional, creates tags if not exist
}
```

#### PATCH /api/todos/{id} - Update Task (Enhanced)

**Request Body**:
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "completed": "boolean (optional)",
  "priority": "none | low | medium | high (optional)",
  "tags": ["work", "urgent"] // optional, replaces existing tags
}
```

### New Endpoints

#### GET /api/tags - List User's Tags

**Response**:
```json
{
  "tags": [
    { "id": "uuid", "name": "work", "task_count": 5 },
    { "id": "uuid", "name": "personal", "task_count": 3 }
  ]
}
```

*Note: Tags are created implicitly when adding to tasks. No separate tag creation endpoint needed.*

---

## Frontend Components

### Priority System

#### PriorityBadge Component

```typescript
// components/tasks/PriorityBadge.tsx
interface PriorityBadgeProps {
  priority: Priority;
  size?: "sm" | "md";
}

// Visual colors following standard conventions
const PRIORITY_COLORS = {
  high: "bg-red-100 text-red-800 border-red-200",
  medium: "bg-yellow-100 text-yellow-800 border-yellow-200",
  low: "bg-blue-100 text-blue-800 border-blue-200",
  none: "bg-gray-100 text-gray-600 border-gray-200",
};
```

#### PrioritySelector Component

```typescript
// In TaskForm - dropdown for priority selection
<Select value={priority} onValueChange={setPriority}>
  <SelectTrigger>
    <SelectValue placeholder="Priority" />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="none">None</SelectItem>
    <SelectItem value="low">Low</SelectItem>
    <SelectItem value="medium">Medium</SelectItem>
    <SelectItem value="high">High</SelectItem>
  </SelectContent>
</Select>
```

### Tag System

#### TagChip Component

```typescript
// components/tasks/TagChip.tsx
interface TagChipProps {
  name: string;
  onRemove?: () => void;  // Show X button if provided
  onClick?: () => void;   // Click to filter
}

// Displays as: [work x] with gray background, clickable
```

#### TagInput Component

```typescript
// components/tasks/TagInput.tsx
interface TagInputProps {
  value: string[];
  onChange: (tags: string[]) => void;
  suggestions: string[];  // From useTags hook
}

// Features:
// - Type to add new tag (single word only)
// - Show suggestions dropdown (sorted alphabetically)
// - Case-insensitive matching to existing tags
// - Validation: no spaces allowed
```

### Search & Filter

#### SearchBar Component

```typescript
// components/tasks/SearchBar.tsx
interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
}

// Features:
// - Debounced input (300ms)
// - Clear button when text present
// - Search icon
```

#### FilterPanel Component

```typescript
// components/tasks/FilterPanel.tsx
interface FilterPanelProps {
  filters: TaskFilters;
  onFiltersChange: (filters: TaskFilters) => void;
  availableTags: string[];
}

interface TaskFilters {
  status: "all" | "pending" | "completed";
  priority: "all" | "high" | "medium" | "low" | "none";
  tags: string[];
  noTags: boolean;
}

// Layout:
// [Status: All | Pending | Completed]
// [Priority: All | High | Medium | Low | None]
// [Tags: Multi-select dropdown with "No tags" option]
// [Clear All Filters] button
```

#### SortSelector Component

```typescript
// components/tasks/SortSelector.tsx
interface SortSelectorProps {
  value: SortOption;
  onChange: (value: SortOption) => void;
}

type SortOption = "priority" | "title" | "created_at";

// Dropdown with options:
// - Priority (highest first) - DEFAULT
// - Title (A to Z)
// - Creation date (newest first)
// Persists to localStorage
```

### State Management

#### useTaskFilters Hook

```typescript
// hooks/useTaskFilters.ts
interface UseTaskFiltersReturn {
  filters: TaskFilters;
  setFilters: (filters: TaskFilters) => void;
  search: string;
  setSearch: (search: string) => void;
  sort: SortOption;
  setSort: (sort: SortOption) => void;  // Persists to localStorage
  clearFilters: () => void;
  hasActiveFilters: boolean;
}
```

#### useTags Hook

```typescript
// hooks/useTags.ts
interface UseTagsReturn {
  tags: Tag[];
  isLoading: boolean;
  fetchTags: () => Promise<void>;
}
```

#### Modified useTasks Hook

```typescript
// hooks/useTasks.ts (modified)
interface FetchTasksParams {
  search?: string;
  status?: "all" | "pending" | "completed";
  priority?: "all" | "high" | "medium" | "low" | "none";
  tags?: string[];
  noTags?: boolean;
  sort?: "priority" | "title" | "created_at";
  order?: "asc" | "desc";
}

interface UseTasksReturn {
  tasks: Task[];
  total: number;       // NEW: Total task count
  filtered: number;    // NEW: Filtered count
  isLoading: boolean;
  error: Error | null;
  fetchTasks: (params?: FetchTasksParams) => Promise<void>;
  createTask: (data: TaskCreateInput) => Promise<Task>;
  updateTask: (id: string, data: TaskUpdateInput) => Promise<Task>;
  deleteTask: (id: string) => Promise<void>;
  toggleTask: (id: string) => Promise<Task>;
}
```

---

## Implementation Strategy

### Phase Order

**Backend First** (data layer must be ready before UI):
1. Database migrations (priority field, tag tables)
2. SQLModel models update
3. Pydantic schemas update
4. CRUD functions update
5. API endpoints update
6. Backend tests

**Frontend Second** (consumes backend API):
1. TypeScript types update
2. Zod schemas update
3. New UI components
4. Hooks update
5. Integration with dashboard
6. Frontend tests

### Migration Strategy

```sql
-- Migration 002: Add priority and tags

-- Step 1: Add priority column with default
ALTER TABLE task ADD COLUMN priority VARCHAR(10) DEFAULT 'none';
CREATE INDEX idx_task_priority ON task(user_id, priority);

-- Step 2: Create tag table
CREATE TABLE tag (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL REFERENCES user(id),
    name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, name)
);
CREATE INDEX idx_tag_user_name ON tag(user_id, name);

-- Step 3: Create junction table
CREATE TABLE task_tag (
    task_id VARCHAR(36) REFERENCES task(id) ON DELETE CASCADE,
    tag_id VARCHAR(36) REFERENCES tag(id) ON DELETE CASCADE,
    PRIMARY KEY (task_id, tag_id)
);
```

### Performance Considerations

1. **Search Debouncing**: 300ms debounce on search input
2. **Database Indexes**: Priority and tag name indexed
3. **Tag Suggestions**: Cached after first fetch
4. **Sort Persistence**: localStorage, not API call
5. **Filtering**: Server-side filtering to reduce payload

---

## Testing Strategy

### Backend Tests

```python
# tests/unit/test_task_crud_filtering.py
def test_list_tasks_with_priority_filter(session, mock_user):
    """Test filtering tasks by priority"""

def test_list_tasks_with_tag_filter(session, mock_user):
    """Test filtering tasks by tags"""

def test_list_tasks_with_search(session, mock_user):
    """Test search in title and description"""

def test_list_tasks_combined_filters(session, mock_user):
    """Test multiple filters with AND logic"""

def test_list_tasks_default_sort(session, mock_user):
    """Test default sort: priority then created_at"""

# tests/unit/test_tag_crud.py
def test_create_tag_lowercase(session, mock_user):
    """Test tag names are stored lowercase"""

def test_create_tag_no_duplicate(session, mock_user):
    """Test case-insensitive tag uniqueness"""

# tests/integration/test_tasks_api_filtering.py
def test_api_filter_by_status(client, mock_auth):
    """Test /api/todos?status=pending"""

def test_api_search(client, mock_auth):
    """Test /api/todos?search=meeting"""
```

### Frontend Tests

```typescript
// tests/components/PriorityBadge.test.tsx
describe('PriorityBadge', () => {
  it('displays correct color for high priority')
  it('displays correct color for none priority')
})

// tests/components/TagInput.test.tsx
describe('TagInput', () => {
  it('prevents tags with spaces')
  it('shows suggestions dropdown')
  it('merges case-insensitive tags')
})

// tests/components/FilterPanel.test.tsx
describe('FilterPanel', () => {
  it('combines multiple filters')
  it('shows clear all button when filters active')
})

// tests/hooks/useTasks.test.ts
describe('useTasks with filters', () => {
  it('sends filter params to API')
  it('returns total and filtered counts')
})
```

---

## Error Handling

### New Validation Errors

**Tag Validation**:
- Spaces in tag: `422 { "detail": "Tags must be single words (no spaces)" }`
- Tag too long: `422 { "detail": "Tag must be 50 characters or less" }`

**Filter Validation**:
- Invalid priority: `422 { "detail": "Invalid priority value" }`
- Invalid status: `422 { "detail": "Invalid status value" }`

### Empty States

```typescript
// When no tasks match filters
<EmptyFilterState
  message="No tasks match your filters"
  onClearFilters={handleClearFilters}
/>

// When no tasks at all
<EmptyState
  message="You don't have any tasks yet"
  action="Create your first task"
/>
```

---

## Success Criteria Mapping

| Criterion | Implementation |
|-----------|----------------|
| SC-001: Priority in <2s | Single click priority dropdown |
| SC-002: New tag <5s | Type + Enter in TagInput |
| SC-003: Existing tag <3s | Click suggestion in dropdown |
| SC-004: Search <300ms | Debounced search, indexed queries |
| SC-005: Filter <500ms | Server-side filtering |
| SC-006: 100+ tasks responsive | Pagination consideration (future), indexed queries |
| SC-007: 320px+ mobile | Tailwind responsive classes |
| SC-008: Clear filters one action | "Clear All" button in FilterPanel |
| SC-009: Sort persists 30+ days | localStorage with no expiry |
| SC-010: Accurate counts | API returns `total` and `filtered` |

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Tag proliferation | Many unused tags | Auto-cleanup orphan tags (no tasks) |
| Search performance | Slow with 100+ tasks | Database indexes, consider full-text search later |
| Filter complexity | Confusing UI | Clear filter indicators, "Clear All" button |
| Mobile UX | Filter panel too large | Collapsible filter section |

---

## Dependencies

- **Existing**: Better Auth, FastAPI, SQLModel, Next.js 16
- **New Backend**: None (use existing patterns)
- **New Frontend**: None (shadcn/ui components already available)

---

## Next Steps

1. Run `/sp.tasks` to generate task breakdown
2. Run `architect-reviewer` subagent to validate plan
3. Execute tasks following Red -> Green -> Refactor cycle
4. Create PHR after implementation

---

**Plan Version**: 1.0.0
**Created**: 2026-01-23
**Author**: Claude Code (Spec-Kit Plus)
