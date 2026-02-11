# Data Model: ChatKit UI Integration (007)

**Feature**: 007-chatkit-ui-integration
**Date**: 2026-02-11

---

## New Tables (ChatKit Protocol)

### chatkit_threads

Stores ChatKit conversation threads. One thread per user session.

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | TEXT | PRIMARY KEY | UUID assigned by ChatKit SDK |
| user_id | TEXT | NOT NULL | Better Auth user ID (`sub` from JWT) |
| created_at | TIMESTAMPTZ | NOT NULL | Thread creation timestamp |
| data | JSONB | NOT NULL | Serialized `ThreadMetadata` object |

**Indexes**: `idx_chatkit_threads_user_id ON chatkit_threads(user_id)`
**User isolation**: All queries filter by `user_id` in WHERE clause

---

### chatkit_items

Stores individual messages (user + assistant) within a thread.

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | TEXT | PRIMARY KEY | UUID assigned by ChatKit SDK |
| thread_id | TEXT | FK → chatkit_threads(id) ON DELETE CASCADE | Parent thread |
| user_id | TEXT | NOT NULL | Same user_id as parent thread |
| created_at | TIMESTAMPTZ | NOT NULL | Message timestamp |
| data | JSONB | NOT NULL | Serialized `ThreadItem` (contains role, content, etc.) |

**Indexes**: `idx_chatkit_items_thread_id ON chatkit_items(thread_id)`
**User isolation**: All queries filter by `user_id` in WHERE clause

---

## Existing Tables (Unchanged)

These tables from feature 006 are NOT used by the ChatKit endpoint. They continue to serve `POST /api/{user_id}/chat`.

| Table | Purpose |
|-------|---------|
| conversation | Stores conversations for stateless JSON endpoint |
| message | Stores messages for stateless JSON endpoint |
| task | User tasks (managed via MCP tools) |
| user | Better Auth user accounts |

---

## ChatKitRequestContext (Python dataclass — not a DB table)

Carries per-request auth + DB session through the ChatKit server pipeline.

| Field | Type | Source |
|-------|------|--------|
| user_id | str | JWT `sub` claim via `get_current_user` dependency |
| session | Session | SQLModel session via `get_session` dependency |

---

## Entity Relationships

```
user (Better Auth)
  │
  └── chatkit_threads (user_id FK)
          │
          └── chatkit_items (thread_id FK, user_id FK)

user
  │
  └── conversation (feature 006 — separate endpoint)
          │
          └── message

user
  └── task (managed by all endpoints via MCP tools)
```
