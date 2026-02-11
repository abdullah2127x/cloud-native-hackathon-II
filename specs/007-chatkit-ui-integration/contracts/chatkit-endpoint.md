# Contract: ChatKit Streaming Endpoint (007)

**Feature**: 007-chatkit-ui-integration
**Date**: 2026-02-11

---

## Backend Endpoint

### POST /chatkit

Processes a ChatKit protocol request and returns either a streaming SSE response or a JSON response.

**Auth**: Bearer JWT required (`Authorization: Bearer <token>`)
**Content-Type**: `application/json` (ChatKit SDK formats the body)

#### Request Body (ChatKit protocol — handled by SDK)

```json
{
  "action": "send_message",
  "thread_id": "thread_abc123",
  "content": "Add buy milk to my tasks"
}
```

Or for new thread:
```json
{
  "action": "send_message",
  "content": "Show my tasks"
}
```

#### Response: Streaming (primary path)

```
HTTP 200
Content-Type: text/event-stream

data: {"type":"text","text":"Your "}
data: {"type":"text","text":"tasks "}
data: {"type":"text","text":"are:..."}
data: [DONE]
```

#### Response: Non-streaming (for thread management actions)

```json
HTTP 200
Content-Type: application/json

{
  "thread_id": "thread_abc123",
  "status": "ok"
}
```

#### Error Responses

| Status | Condition |
|--------|-----------|
| 401 | Missing or invalid Bearer token |
| 404 | Thread not found or belongs to another user |
| 503 | AI provider (OpenRouter) unavailable |
| 422 | Invalid request body |

---

## Frontend Integration

### ChatKit UI Component Configuration

The Next.js `ChatKit` component is configured to point at the backend:

```typescript
<ChatKit
  api={{
    url: `${process.env.NEXT_PUBLIC_BACKEND_URL}/chatkit`,
    headers: {
      Authorization: `Bearer ${getJwtToken()}`
    }
  }}
/>
```

### Route

New page: `/dashboard/chat` — accessible from the dashboard sidebar nav.

### Auth Header

JWT token retrieved via `getJwtToken()` from `@/lib/auth-client` (stored in localStorage as `better_auth_jwt`).

---

## Backend File Structure

```
backend/src/
├── chatkit/
│   ├── __init__.py
│   ├── store.py          ← PostgresStore implementation
│   └── server.py         ← TodoChatKitServer (ChatKitServer subclass)
└── routers/
    └── chatkit.py        ← POST /chatkit FastAPI router
```

## Frontend File Structure

```
frontend/src/app/dashboard/
├── chat/
│   └── page.tsx          ← Chat page with ChatKit UI component
└── components/
    └── Sidebar.tsx        ← Add "Chat" nav item (existing file, small edit)
```
