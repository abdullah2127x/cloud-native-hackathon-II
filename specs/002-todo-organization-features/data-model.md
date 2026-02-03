# Data Model: Todo Organization Features

**Feature**: 002-todo-organization-features
**Date**: 2026-01-23
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## Overview

This document defines the database schema changes required for Phase 2 organization features: priorities, tags, search, filtering, and sorting.

---

## Schema Changes

### 1. Priority Enum

```python
# backend/src/models/priority.py
from enum import Enum

class Priority(str, Enum):
    """
    Task priority levels.

    Values are strings for JSON serialization and database storage.
    Sort order is defined separately for query optimization.
    """
    NONE = "none"      # Default, lowest sort priority
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# Sort order mapping (lower = higher priority in sort)
PRIORITY_SORT_ORDER = {
    Priority.HIGH: 0,
    Priority.MEDIUM: 1,
    Priority.LOW: 2,
    Priority.NONE: 3,
}
```

### 2. Extended Task Model

```python
# backend/src/models/task.py (modified)
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, UTC
from typing import Optional, List
import uuid

from src.models.priority import Priority


def utc_now() -> datetime:
    """Get current UTC time"""
    return datetime.now(UTC)


def generate_uuid() -> str:
    """Generate UUID string"""
    return str(uuid.uuid4())


class Task(SQLModel, table=True):
    """
    Task model for user todo items.

    Spec: 002-todo-organization-features
    Extended from 001-todo-web-crud with:
    - priority field (enum)
    - tags relationship (many-to-many)
    """

    # Primary key
    id: str = Field(default_factory=generate_uuid, primary_key=True)

    # Foreign key - CRITICAL: All queries must filter by this
    user_id: str = Field(foreign_key="user.id", index=True)

    # Task content
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)

    # Status
    completed: bool = Field(default=False)

    # NEW: Priority level
    priority: Priority = Field(default=Priority.NONE, index=True)

    # Timestamps
    created_at: datetime = Field(default_factory=utc_now, index=True)
    updated_at: Optional[datetime] = Field(default=None)

    # NEW: Relationship to tags (via junction table)
    tags: List["Tag"] = Relationship(
        back_populates="tasks",
        link_model="TaskTag"
    )
```

### 3. Tag Model (New)

```python
# backend/src/models/tag.py
from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from datetime import datetime, UTC
from typing import List, TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from src.models.task import Task


def utc_now() -> datetime:
    return datetime.now(UTC)


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Tag(SQLModel, table=True):
    """
    Tag for categorizing tasks.

    Spec: 002-todo-organization-features

    Constraints:
    - Unique per user (user_id + name)
    - Names are stored lowercase
    - No spaces allowed (single word only)
    - Max 50 characters
    """
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_tag_user_name"),
    )

    # Primary key
    id: str = Field(default_factory=generate_uuid, primary_key=True)

    # Foreign key - tags are user-scoped
    user_id: str = Field(foreign_key="user.id", index=True)

    # Tag name (lowercase, no spaces)
    name: str = Field(max_length=50, index=True)

    # Timestamp
    created_at: datetime = Field(default_factory=utc_now)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(
        back_populates="tags",
        link_model="TaskTag"
    )


class TaskTag(SQLModel, table=True):
    """
    Junction table for Task-Tag many-to-many relationship.

    Spec: 002-todo-organization-features
    """
    __tablename__ = "task_tag"

    task_id: str = Field(
        foreign_key="task.id",
        primary_key=True,
        ondelete="CASCADE"
    )
    tag_id: str = Field(
        foreign_key="tag.id",
        primary_key=True,
        ondelete="CASCADE"
    )
```

---

## Database Indexes

### Existing Indexes (from Phase 1)

```sql
-- Task table
CREATE INDEX idx_task_user_id ON task(user_id);
CREATE INDEX idx_task_created_at ON task(created_at);
```

### New Indexes (Phase 2)

```sql
-- Priority filtering
CREATE INDEX idx_task_user_priority ON task(user_id, priority);

-- Completion status filtering
CREATE INDEX idx_task_user_completed ON task(user_id, completed);

-- Composite index for default sort (priority then created_at)
CREATE INDEX idx_task_user_priority_created ON task(user_id, priority, created_at DESC);

-- Tag lookup by user
CREATE INDEX idx_tag_user_id ON tag(user_id);

-- Tag lookup by name (for case-insensitive matching)
CREATE INDEX idx_tag_user_name ON tag(user_id, name);

-- Junction table indexes (auto-created for PKs, but explicit for joins)
CREATE INDEX idx_task_tag_task ON task_tag(task_id);
CREATE INDEX idx_task_tag_tag ON task_tag(tag_id);
```

---

## Migration Script

```sql
-- Migration: 002_add_priority_and_tags
-- Date: 2026-01-23
-- Spec: 002-todo-organization-features

-- ============================================
-- Step 1: Add priority column to task table
-- ============================================

-- Add column with default value
ALTER TABLE task
ADD COLUMN priority VARCHAR(10) NOT NULL DEFAULT 'none';

-- Add check constraint for valid values
ALTER TABLE task
ADD CONSTRAINT chk_task_priority
CHECK (priority IN ('none', 'low', 'medium', 'high'));

-- Add indexes for priority filtering
CREATE INDEX idx_task_user_priority ON task(user_id, priority);
CREATE INDEX idx_task_user_completed ON task(user_id, completed);
CREATE INDEX idx_task_user_priority_created ON task(user_id, priority, created_at DESC);

-- ============================================
-- Step 2: Create tag table
-- ============================================

CREATE TABLE tag (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),

    -- Foreign key to user
    CONSTRAINT fk_tag_user
        FOREIGN KEY (user_id)
        REFERENCES "user"(id)
        ON DELETE CASCADE,

    -- Unique tag name per user
    CONSTRAINT uq_tag_user_name
        UNIQUE (user_id, name)
);

-- Indexes for tag lookup
CREATE INDEX idx_tag_user_id ON tag(user_id);
CREATE INDEX idx_tag_user_name ON tag(user_id, name);

-- ============================================
-- Step 3: Create task_tag junction table
-- ============================================

CREATE TABLE task_tag (
    task_id VARCHAR(36) NOT NULL,
    tag_id VARCHAR(36) NOT NULL,

    -- Composite primary key
    PRIMARY KEY (task_id, tag_id),

    -- Foreign keys with cascade delete
    CONSTRAINT fk_task_tag_task
        FOREIGN KEY (task_id)
        REFERENCES task(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_task_tag_tag
        FOREIGN KEY (tag_id)
        REFERENCES tag(id)
        ON DELETE CASCADE
);

-- Indexes for join performance
CREATE INDEX idx_task_tag_task ON task_tag(task_id);
CREATE INDEX idx_task_tag_tag ON task_tag(tag_id);
```

---

## Pydantic Schemas

### Request Schemas

```python
# backend/src/schemas/task.py (extended)
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List
import re

from src.models.priority import Priority


class TaskCreate(BaseModel):
    """Schema for creating a new task"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    priority: Priority = Field(default=Priority.NONE)
    tags: List[str] = Field(default_factory=list, max_length=20)  # Max 20 tags

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v: List[str]) -> List[str]:
        """Validate tag format: lowercase, no spaces, max 50 chars"""
        validated = []
        for tag in v:
            # Check for spaces
            if ' ' in tag:
                raise ValueError(f"Tag '{tag}' cannot contain spaces")
            # Check length
            if len(tag) > 50:
                raise ValueError(f"Tag '{tag}' exceeds 50 characters")
            if len(tag) < 1:
                raise ValueError("Tag cannot be empty")
            # Convert to lowercase and dedupe
            lower_tag = tag.lower()
            if lower_tag not in validated:
                validated.append(lower_tag)
        return validated


class TaskUpdate(BaseModel):
    """Schema for updating an existing task"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    completed: Optional[bool] = None
    priority: Optional[Priority] = None
    tags: Optional[List[str]] = Field(None, max_length=20)

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validate tag format if provided"""
        if v is None:
            return None
        validated = []
        for tag in v:
            if ' ' in tag:
                raise ValueError(f"Tag '{tag}' cannot contain spaces")
            if len(tag) > 50:
                raise ValueError(f"Tag '{tag}' exceeds 50 characters")
            if len(tag) < 1:
                raise ValueError("Tag cannot be empty")
            lower_tag = tag.lower()
            if lower_tag not in validated:
                validated.append(lower_tag)
        return validated
```

### Response Schemas

```python
# backend/src/schemas/task.py (continued)

class TagRead(BaseModel):
    """Schema for tag response"""
    id: str
    name: str
    task_count: int = 0  # Number of tasks with this tag

    class Config:
        from_attributes = True


class TaskRead(BaseModel):
    """Schema for task response"""
    id: str
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    priority: Priority
    tags: List[str]  # Just tag names, not full objects
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Schema for paginated task list response"""
    tasks: List[TaskRead]
    total: int      # Total tasks for user
    filtered: int   # Tasks matching current filters


class TagListResponse(BaseModel):
    """Schema for tag list response"""
    tags: List[TagRead]
```

### Query Parameters Schema

```python
# backend/src/schemas/task.py (continued)
from enum import Enum


class StatusFilter(str, Enum):
    """Task status filter options"""
    ALL = "all"
    PENDING = "pending"
    COMPLETED = "completed"


class PriorityFilter(str, Enum):
    """Priority filter options (includes 'all')"""
    ALL = "all"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"


class SortField(str, Enum):
    """Available sort fields"""
    PRIORITY = "priority"
    TITLE = "title"
    CREATED_AT = "created_at"


class SortOrder(str, Enum):
    """Sort direction"""
    ASC = "asc"
    DESC = "desc"


class TaskQueryParams(BaseModel):
    """Query parameters for task list endpoint"""
    search: Optional[str] = Field(None, max_length=200)
    status: StatusFilter = Field(default=StatusFilter.ALL)
    priority: PriorityFilter = Field(default=PriorityFilter.ALL)
    tags: Optional[List[str]] = None
    no_tags: bool = False
    sort: SortField = Field(default=SortField.PRIORITY)
    order: Optional[SortOrder] = None  # Default depends on sort field
```

---

## TypeScript Types (Frontend)

```typescript
// frontend/src/types/task.ts (extended)

/**
 * Priority levels for tasks
 * Spec: 002-todo-organization-features
 */
export type Priority = 'none' | 'low' | 'medium' | 'high';

/**
 * Tag type
 * Spec: 002-todo-organization-features
 */
export interface Tag {
  id: string;
  name: string;
  task_count: number;
}

/**
 * Extended Task interface with priority and tags
 * Spec: 002-todo-organization-features
 */
export interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  priority: Priority;
  tags: string[];  // Tag names
  created_at: string;
  updated_at: string | null;
}

/**
 * Task creation input
 */
export interface TaskCreateInput {
  title: string;
  description?: string;
  priority?: Priority;
  tags?: string[];
}

/**
 * Task update input
 */
export interface TaskUpdateInput {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: Priority;
  tags?: string[];
}

/**
 * Task list API response
 */
export interface TaskListResponse {
  tasks: Task[];
  total: number;
  filtered: number;
}

/**
 * Filter state for task list
 */
export interface TaskFilters {
  status: 'all' | 'pending' | 'completed';
  priority: 'all' | 'high' | 'medium' | 'low' | 'none';
  tags: string[];
  noTags: boolean;
}

/**
 * Sort options
 */
export type SortField = 'priority' | 'title' | 'created_at';
export type SortOrder = 'asc' | 'desc';
```

---

## Entity Relationship Diagram

```
┌──────────────────┐
│      user        │
├──────────────────┤
│ id (PK)          │
│ email            │
│ name             │
│ ...              │
└────────┬─────────┘
         │
         │ 1:N
         ▼
┌──────────────────┐       ┌──────────────────┐
│      task        │       │       tag        │
├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │
│ user_id (FK)     │───────│ user_id (FK)     │
│ title            │       │ name             │
│ description      │       │ created_at       │
│ completed        │       └────────┬─────────┘
│ priority         │                │
│ created_at       │                │
│ updated_at       │                │
└────────┬─────────┘                │
         │                          │
         │ M:N                      │
         │                          │
         ▼                          ▼
┌────────────────────────────────────┐
│           task_tag                 │
├────────────────────────────────────┤
│ task_id (PK, FK)                   │
│ tag_id (PK, FK)                    │
└────────────────────────────────────┘
```

---

## Data Constraints Summary

| Entity | Field | Constraint |
|--------|-------|------------|
| Task | priority | Enum: none, low, medium, high |
| Task | priority | Default: none |
| Tag | name | Max 50 characters |
| Tag | name | No spaces (single word) |
| Tag | name | Stored lowercase |
| Tag | (user_id, name) | Unique per user |
| Task | tags | Max 20 tags per task |

---

## Query Patterns

### Default Task List (Priority Sort)

```sql
SELECT t.*, array_agg(tg.name) as tags
FROM task t
LEFT JOIN task_tag tt ON t.id = tt.task_id
LEFT JOIN tag tg ON tt.tag_id = tg.id
WHERE t.user_id = :user_id
GROUP BY t.id
ORDER BY
    CASE t.priority
        WHEN 'high' THEN 0
        WHEN 'medium' THEN 1
        WHEN 'low' THEN 2
        WHEN 'none' THEN 3
    END,
    t.created_at DESC
```

### Filtered Task List

```sql
SELECT t.*, array_agg(tg.name) as tags
FROM task t
LEFT JOIN task_tag tt ON t.id = tt.task_id
LEFT JOIN tag tg ON tt.tag_id = tg.id
WHERE t.user_id = :user_id
  AND (:search IS NULL OR (
       t.title ILIKE '%' || :search || '%' OR
       t.description ILIKE '%' || :search || '%'))
  AND (:status = 'all' OR
       (:status = 'pending' AND t.completed = false) OR
       (:status = 'completed' AND t.completed = true))
  AND (:priority = 'all' OR t.priority = :priority)
GROUP BY t.id
HAVING (:no_tags = false OR array_length(array_agg(tg.name), 1) IS NULL)
   AND (:tags IS NULL OR array_agg(tg.name) && :tags)
ORDER BY ...
```

### Get User's Tags with Count

```sql
SELECT tg.id, tg.name, COUNT(tt.task_id) as task_count
FROM tag tg
LEFT JOIN task_tag tt ON tg.id = tt.tag_id
LEFT JOIN task t ON tt.task_id = t.id AND t.user_id = :user_id
WHERE tg.user_id = :user_id
GROUP BY tg.id, tg.name
ORDER BY tg.name ASC
```

---

**Document Version**: 1.0.0
**Created**: 2026-01-23
**Author**: Claude Code (Spec-Kit Plus)
