# Frontend API Contract: Modern UI Dashboard

**Feature**: 003-modern-ui-dashboard
**Date**: 2026-01-29
**Purpose**: Define frontend interaction patterns with backend APIs

## Overview

This feature uses **existing backend APIs** without modifications. All interactions follow the existing contract established in previous features.

## Authentication API (Better Auth)

### Session Management

**Endpoint**: `/api/auth/session` (via Better Auth client)
**Method**: GET
**Authentication**: Not required (checks JWT in localStorage)

**Response**:
```typescript
{
  session: {
    user: {
      id: string;
      email: string;
      name?: string;
      emailVerified: boolean;
    };
    token: string;
    expiresAt: number;
  } | null
}
```

**Usage in Feature**:
- Check authentication status on app load
- Redirect unauthenticated users to `/sign-in`
- Display user email/name in dashboard navigation
- Implement logout functionality

**Implementation**: Existing `useSession()` hook (no changes)

---

### Sign In

**Endpoint**: `/api/auth/sign-in` (via Better Auth client)
**Method**: POST

**Request**:
```typescript
{
  email: string;
  password: string;
}
```

**Response**:
```typescript
{
  token: string;
  user: {
    id: string;
    email: string;
    name?: string;
  }
}
```

**Usage in Feature**:
- `/sign-in` page form submission
- Redirect to `/dashboard/overview` on success
- Display error messages on failure

**Implementation**: Existing `SignInForm` component (reuse with no changes)

---

### Sign Out

**Endpoint**: Via Better Auth client
**Method**: Logout action

**Implementation**:
```typescript
const { signOut } = useAuth();
await signOut();
// Redirect to /sign-in
```

**Usage in Feature**:
- Dashboard navigation logout button
- Clear JWT token from localStorage
- Redirect to `/sign-in`

---

## Todo API (FastAPI Backend)

### List Todos

**Endpoint**: `GET /api/todos`
**Authentication**: Required (JWT in Authorization header)

**Query Parameters**:
- `search?` (string) - Search title/description
- `status?` ("all" | "pending" | "completed") - Filter by completion
- `priority?` ("high" | "medium" | "low" | "none" | "all") - Filter by priority
- `tags?` (string[]) - Filter by tags (OR logic)
- `no_tags?` (boolean) - Filter todos without tags
- `sort?` ("priority" | "title" | "created_at") - Sort field
- `order?` ("asc" | "desc") - Sort direction

**Response**:
```typescript
{
  tasks: Todo[];
  total: number;
  filtered: number;
}

interface Todo {
  id: string;
  title: string;
  description: string | null;
  completed: boolean;
  priority: "high" | "medium" | "low" | "none";
  created_at: string;
  updated_at: string | null;
  tags: string[];
}
```

**Usage in Feature**:
- Fetch todos for All Todos page (with filters/search)
- Fetch todos by priority (Priority page)
- Fetch todos by tags (Tags page)
- Calculate statistics (Overview page)

**Implementation**: Existing `useTasks().fetchTasks(params)` method

---

### Create Todo

**Endpoint**: `POST /api/todos`
**Authentication**: Required (JWT in Authorization header)

**Request**:
```typescript
{
  title: string;           // Required, max 200 chars
  description?: string;    // Optional, max 2000 chars
  priority?: "high" | "medium" | "low" | "none"; // Default: "none"
  tags?: string[];         // Optional, max 20 tags, each max 50 chars
}
```

**Response** (201 Created):
```typescript
{
  id: string;
  title: string;
  description: string | null;
  completed: boolean;
  priority: "high" | "medium" | "low" | "none";
  created_at: string;
  updated_at: string | null;
  tags: string[];
}
```

**Error Responses**:
- `422 Validation Error` - Invalid input (missing title, too long, etc.)
- `401 Unauthorized` - Invalid or missing JWT
- `500 Internal Server Error` - Server error

**Usage in Feature**:
- Add Todo dialog form submission (All Todos page)
- Create new todo with title, description, priority, tag
- Show Toast notification on success/error

**Implementation**: Existing `useTasks().createTask(data)` method

---

### Get Single Todo

**Endpoint**: `GET /api/todos/:id`
**Authentication**: Required (JWT in Authorization header)

**Response**:
```typescript
{
  id: string;
  title: string;
  description: string | null;
  completed: boolean;
  priority: "high" | "medium" | "low" | "none";
  created_at: string;
  updated_at: string | null;
  tags: string[];
}
```

**Usage in Feature**:
- Pre-populate Edit todo form with existing data

**Note**: Not explicitly called - Todo list already contains full data

---

### Update Todo

**Endpoint**: `PATCH /api/todos/:id`
**Authentication**: Required (JWT in Authorization header)

**Request** (partial update):
```typescript
{
  title?: string;
  description?: string;
  priority?: "high" | "medium" | "low" | "none";
  tags?: string[];
  // completed should use /toggle endpoint instead
}
```

**Response** (200 OK):
```typescript
{
  id: string;
  title: string;
  description: string | null;
  completed: boolean;
  priority: "high" | "medium" | "low" | "none";
  created_at: string;
  updated_at: string | null;
  tags: string[];
}
```

**Usage in Feature**:
- Edit Todo dialog form submission (All Todos page)
- Update title, description, priority, or tags
- Show Toast notification on success/error

**Implementation**: Existing `useTasks().updateTask(id, data)` method

---

### Delete Todo

**Endpoint**: `DELETE /api/todos/:id`
**Authentication**: Required (JWT in Authorization header)

**Response**: 204 No Content

**Error Responses**:
- `401 Unauthorized` - Invalid or missing JWT
- `404 Not Found` - Todo not found or not owned by user
- `500 Internal Server Error` - Server error

**Usage in Feature**:
- Delete confirm AlertDialog button (All Todos page)
- Permanently remove todo from database
- Show Toast notification on success/error

**Implementation**: Existing `useTasks().deleteTask(id)` method

---

### Toggle Todo Completion

**Endpoint**: `POST /api/todos/:id/toggle`
**Authentication**: Required (JWT in Authorization header)

**Request**: No body

**Response** (200 OK):
```typescript
{
  id: string;
  title: string;
  description: string | null;
  completed: boolean;  // Toggled value
  priority: "high" | "medium" | "low" | "none";
  created_at: string;
  updated_at: string | null;
  tags: string[];
}
```

**Usage in Feature**:
- Todo completion checkbox click (All Todos, Priority, Tags pages)
- Toggle between completed and pending states
- Show Toast notification
- Update visual styling (gray background, strikethrough)

**Implementation**: Existing `useTasks().toggleTask(id)` method

---

## Error Handling

### API Errors
All API errors are handled via existing Axios interceptor (`src/middleware/api-interceptor.ts`):

**401 Unauthorized**:
- Clear JWT token from localStorage
- Redirect to `/sign-in` with `returnUrl` parameter
- Show "Session expired" message

**422 Validation Error**:
- Extract validation errors from response
- Display in Toast notification or form field errors
- Preserve form data for correction

**500 Server Error**:
- Display generic error message: "An error occurred. Please try again."
- Show in Toast notification
- Log for debugging

**Network Error**:
- Show "Network error. Please check your connection."
- Provide retry option in Toast

---

## Request Headers

All requests automatically include (via Axios interceptor):
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

Where `jwt_token` is retrieved from localStorage key: `better_auth_jwt`

---

## Frontend API Usage Patterns

### Todos Page (All Todos)

```typescript
// Fetch todos with filters
const { tasks, fetchTasks } = useTasks();

// On page load
useEffect(() => {
  fetchTasks({
    status: filter,      // "all" | "pending" | "completed"
    search: searchText,
    priority: selectedPriority,
    tags: selectedTags,
    sort: sortBy,
    order: sortOrder
  });
}, [filter, searchText, selectedPriority, selectedTags, sortBy, sortOrder]);

// Create todo
const handleCreate = async (formData) => {
  const newTodo = await createTask(formData);
  // UI updated automatically via hook state
};

// Update todo
const handleUpdate = async (id, formData) => {
  const updated = await updateTask(id, formData);
  // UI updated automatically
};

// Delete todo
const handleDelete = async (id) => {
  await deleteTask(id);
  // Refetch todos to update counts
};

// Toggle completion
const handleToggle = async (id) => {
  await toggleTask(id);
  // UI updated automatically
};
```

### Overview Page (Statistics)

```typescript
// Fetch all todos (unfiltered)
const { tasks } = useTasks();

// Compute statistics
const stats = {
  total: tasks.length,
  completed: tasks.filter(t => t.completed).length,
  pending: tasks.filter(t => !t.completed).length,
  today: tasks.filter(t => isToday(t.created_at)).length
};

// Display in stat cards
```

### Priority Page (By Priority)

```typescript
// Fetch todos for High priority
const { tasks } = useTasks();

const highPriorityTodos = tasks.filter(t => t.priority === "high");
const mediumPriorityTodos = tasks.filter(t => t.priority === "medium");
const lowPriorityTodos = tasks.filter(t => t.priority === "low");

// Display in priority tabs/sections
```

### Tags Page (By Tags)

```typescript
// Extract unique tags from all todos
const { tasks } = useTasks();

const uniqueTags = [...new Set(tasks.flatMap(t => t.tags))].sort();

// Filter todos by selected tag
const filteredTodos = tasks.filter(t => t.tags.includes(selectedTag));

// Display as clickable badge list
```

---

## Performance Considerations

### Caching
- Browser caches GET /api/todos responses per request parameters
- No explicit cache headers - rely on Axios default behavior

### Pagination
- API supports all user's todos in single request
- No pagination in this phase (Assumption #11)
- Frontend filters/sorts in-memory if needed

### Real-time Updates
- No real-time sync between devices (Assumption #12)
- Manual page refresh needed for multi-device scenarios

---

## Contract Versioning

**Version**: 1.0
**Status**: Production (existing APIs)
**Last Updated**: 2026-01-29
**Compatibility**: All requests compatible with existing FastAPI backend

---

## No Breaking Changes

✅ All feature requirements map to existing endpoints
✅ No new endpoints required
✅ No request/response format changes
✅ No authentication mechanism changes
✅ Existing Axios interceptor handles all API communication

**Contract is backward compatible with existing implementation.**
