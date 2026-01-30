# Data Model: Modern UI Dashboard Transformation

**Feature**: 003-modern-ui-dashboard
**Date**: 2026-01-29
**Purpose**: Define data structures and relationships for UI transformation

## Overview

This feature is a **frontend-only transformation** that does not introduce new data entities or modify the existing database schema. All data models already exist and are fully functional.

## Existing Data Entities (No Changes)

### User
**Source**: Better Auth managed entity
**Location**: Database (Better Auth tables)

**Fields**:
- `id` (string, UUID) - Primary key
- `email` (string) - User email address
- `name` (string, optional) - User display name
- `createdAt` (datetime) - Account creation timestamp

**Relationships**:
- One-to-Many with `Todo` (user owns multiple todos)

**Usage in Feature**:
- Display user email/name in dashboard navigation
- Filter all todos by user ID (user isolation)
- Logout functionality

**No Changes Required**: ✅ Existing Better Auth implementation

---

### Todo (Task)
**Source**: Existing application entity
**Location**: `backend/src/models/task.py`, `frontend/src/types/task.ts`
**Database Table**: `task`

**Fields**:
- `id` (string, UUID) - Primary key
- `user_id` (string, UUID, FK) - Owner reference
- `title` (string, max 200 chars, required) - Todo title
- `description` (string, max 2000 chars, optional) - Todo description
- `completed` (boolean, default false) - Completion status
- `priority` (enum: "high" | "medium" | "low" | "none", default "none") - Priority level
- `created_at` (datetime, UTC) - Creation timestamp
- `updated_at` (datetime, UTC, optional) - Last modification timestamp
- `tags` (array of strings) - Associated tags (many-to-many relationship)

**Relationships**:
- Many-to-One with `User` (todo belongs to user)
- Many-to-Many with `Tag` (via TaskTag junction table)

**Validation Rules**:
- Title: Required, max 200 characters
- Description: Optional, max 2000 characters
- Priority: Must be one of enum values
- Tags: Max 20 tags per todo, each tag max 50 characters, single word only

**State Transitions**:
- `completed: false` ⟷ `completed: true` (toggle)

**Usage in Feature**:
- Display in todo cards (All Todos, Priority, Tags pages)
- Filter by priority (Priority page)
- Filter by tags (Tags page)
- Filter by completion status (All/Active/Completed)
- Calculate statistics (Overview page)

**No Changes Required**: ✅ Existing implementation fully supports all features

---

### Tag
**Source**: Existing application entity
**Location**: `backend/src/models/tag.py`, `frontend/src/types/task.ts`
**Database Table**: `tag`

**Fields**:
- `id` (string, UUID) - Primary key
- `user_id` (string, UUID, FK) - Owner reference
- `name` (string, max 50 chars, lowercase) - Tag name

**Relationships**:
- Many-to-One with `User` (tag belongs to user)
- Many-to-Many with `Todo` (via TaskTag junction table)

**Validation Rules**:
- Name: Required, max 50 characters, single word (no spaces), lowercase
- Unique per user (case-insensitive)

**Usage in Feature**:
- Display as badges on todo cards
- Display as clickable badges on Tags page
- Filter todos by tag

**No Changes Required**: ✅ Existing implementation fully supports all features

---

### Priority Level
**Source**: Existing enum
**Location**: `backend/src/models/priority.py`, `frontend/src/lib/validations/task.ts`

**Values**:
- `"high"` - Highest priority (red/destructive color)
- `"medium"` - Medium priority (yellow/warning color)
- `"low"` - Low priority (green/default color)
- `"none"` - No priority set (gray color)

**Usage in Feature**:
- Display as colored badges on todo cards
- Filter todos by priority (Priority page tabs/sections)
- Sort todos by priority

**Visual Mapping** (Frontend Only):
```typescript
const priorityConfig = {
  high: { label: "High", color: "destructive", variant: "destructive" },
  medium: { label: "Medium", color: "warning", variant: "default" },
  low: { label: "Low", color: "success", variant: "default" },
  none: { label: "None", color: "secondary", variant: "secondary" }
}
```

**No Changes Required**: ✅ Existing implementation, only UI presentation changes

---

## New UI-Only Data Structures (Frontend State)

These are **computed/derived values** and **UI state**, not database entities.

### DashboardStatistics (Computed)
**Purpose**: Calculate todo counts for Overview page
**Source**: Derived from existing `Todo[]` data
**Location**: Frontend only (computed in component or hook)

**Fields**:
```typescript
interface DashboardStatistics {
  total: number;           // All todos for user
  completed: number;       // Todos where completed = true
  pending: number;         // Todos where completed = false
  today: number;           // Todos created today (createdAt >= start of day)
}
```

**Calculation Logic**:
```typescript
const calculateStats = (todos: Todo[]): DashboardStatistics => {
  const today = new Date().setHours(0, 0, 0, 0);

  return {
    total: todos.length,
    completed: todos.filter(t => t.completed).length,
    pending: todos.filter(t => !t.completed).length,
    today: todos.filter(t => new Date(t.created_at).setHours(0, 0, 0, 0) >= today).length
  };
};
```

**Usage**: Overview page stat cards

---

### NavigationSection (UI State)
**Purpose**: Define dashboard navigation structure
**Location**: Frontend constants/config

**Structure**:
```typescript
interface NavigationSection {
  id: string;              // Unique identifier (matches route)
  label: string;           // Display text
  icon: LucideIcon;        // Icon component
  href: string;            // Route path
  badge?: number;          // Optional count badge
}

const navigationSections: NavigationSection[] = [
  { id: "overview", label: "Overview", icon: LayoutDashboard, href: "/dashboard/overview" },
  { id: "todos", label: "All Todos", icon: CheckSquare, href: "/dashboard/todos" },
  { id: "priority", label: "By Priority", icon: Flag, href: "/dashboard/priority" },
  { id: "tags", label: "By Tags", icon: Tag, href: "/dashboard/tags" },
  { id: "settings", label: "Settings", icon: Settings, href: "/dashboard/settings" }
];
```

**Usage**: Sidebar and mobile navigation menu

---

### MobileMenuState (UI State)
**Purpose**: Track mobile hamburger menu open/closed state
**Location**: Dashboard layout component

**Structure**:
```typescript
const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
```

**Usage**: Control Sheet component visibility on mobile

---

### FormDialogState (UI State)
**Purpose**: Control Add/Edit todo dialog visibility and mode
**Location**: Todos page component

**Structure**:
```typescript
interface TodoFormState {
  open: boolean;           // Dialog open/closed
  mode: "create" | "edit"; // Form mode
  todo?: Todo;             // Existing todo (edit mode only)
}

const [formState, setFormState] = useState<TodoFormState>({
  open: false,
  mode: "create",
  todo: undefined
});
```

**Usage**: Control Dialog component and form pre-population

---

### DeleteConfirmationState (UI State)
**Purpose**: Control delete confirmation AlertDialog
**Location**: Todo card component

**Structure**:
```typescript
interface DeleteConfirmState {
  open: boolean;
  todoId: string | null;
}

const [deleteConfirm, setDeleteConfirm] = useState<DeleteConfirmState>({
  open: false,
  todoId: null
});
```

**Usage**: Control AlertDialog for delete confirmation

---

## Data Flow

### Overview Page Statistics
```
Backend API → useTasks() hook → todos[]
                                   ↓
                          calculateStats(todos)
                                   ↓
                            DashboardStatistics
                                   ↓
                            StatCard components
```

### Todo Display (All Pages)
```
Backend API → useTasks() hook → todos[]
                                   ↓
                          Filter/Sort (if needed)
                                   ↓
                              TodoCard[]
                                   ↓
                         shadcn Card components
```

### Todo CRUD Operations
```
User Action → Component Event → useTasks() method → Axios + JWT → Backend API
                                                                      ↓
                                                              Database Update
                                                                      ↓
                                                            Response + Optimistic UI
                                                                      ↓
                                                              Toast Notification
```

### Navigation Active State
```
Next.js Router → usePathname() → currentPath
                                      ↓
                             Match against sections
                                      ↓
                            Highlight active section
```

---

## API Contract (No Changes)

All existing API endpoints remain unchanged. This feature uses existing endpoints:

### Authentication (Better Auth)
- `POST /api/auth/sign-in` - Sign in user
- `POST /api/auth/sign-up` - Create account
- `POST /api/auth/sign-out` - Sign out user
- `GET /api/auth/session` - Get current session

### Todos (FastAPI Backend)
- `GET /api/todos` - List todos with filters (search, status, priority, tags, sort)
- `POST /api/todos` - Create todo
- `GET /api/todos/:id` - Get single todo
- `PATCH /api/todos/:id` - Update todo
- `DELETE /api/todos/:id` - Delete todo
- `POST /api/todos/:id/toggle` - Toggle completion

**No New Endpoints Required**: ✅ All data access covered by existing API

---

## Database Schema (No Changes)

**Existing Tables**:
- `user` (Better Auth managed)
- `task` (todos)
- `tag` (user tags)
- `task_tag` (junction table)

**No Migrations Required**: ✅ Schema fully supports all feature requirements

---

## Type Definitions (Frontend)

All existing TypeScript types remain valid. No new entity types needed.

### Existing Types (Reuse)
```typescript
// frontend/src/types/task.ts
interface Todo {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  priority: "high" | "medium" | "low" | "none";
  created_at: string;
  updated_at: string | null;
  tags: string[];
}

interface User {
  id: string;
  email: string;
  name: string | null;
}
```

### New UI Types (Component Props/State)
```typescript
// Dashboard statistics (computed)
interface DashboardStatistics {
  total: number;
  completed: number;
  pending: number;
  today: number;
}

// Navigation section
interface NavigationSection {
  id: string;
  label: string;
  icon: LucideIcon;
  href: string;
  badge?: number;
}

// Form dialog state
interface TodoFormState {
  open: boolean;
  mode: "create" | "edit";
  todo?: Todo;
}

// Delete confirmation state
interface DeleteConfirmState {
  open: boolean;
  todoId: string | null;
}
```

---

## Validation Rules (No Changes)

All validation rules remain as defined in existing Zod schemas:

**Todo Validation** (`frontend/src/lib/validations/task.ts`):
- Title: Required, max 200 chars
- Description: Optional, max 2000 chars
- Priority: Enum ("high" | "medium" | "low" | "none")
- Tag: Optional, single word, max 50 chars

**No New Validation Required**: ✅ Existing schemas cover all form inputs

---

## Summary

### Data Model Changes
- ✅ **Zero database schema changes**
- ✅ **Zero new backend entities**
- ✅ **Zero new API endpoints**
- ✅ **Zero data model modifications**

### What's New
- ✅ **UI-only computed values** (statistics)
- ✅ **UI-only state** (navigation, dialogs, menus)
- ✅ **Frontend type definitions** (component props/state)
- ✅ **Visual presentation** (layouts, components, styling)

### Constitutional Compliance
- ✅ **VIII. Persistent Storage**: No changes to persistence layer
- ✅ **IX. RESTful API**: Reuses existing API, no modifications
- ✅ **X. Security & User Isolation**: Existing backend enforcement continues
- ✅ **XI. Authentication**: Better Auth unchanged
- ✅ **XII. Architecture**: Frontend-only changes, monorepo structure maintained

**Conclusion**: This is a pure **UI transformation** with zero backend/database changes. All data access uses existing, fully-functional APIs and data models.
