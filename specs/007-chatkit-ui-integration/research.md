# Research: ChatKit UI Integration (007)

**Feature**: 007-chatkit-ui-integration
**Date**: 2026-02-11
**Sources**: chatkit-server skill references (openai/chatkit-python Context7), existing codebase inspection

---

## Decision 1: Backend streaming protocol — ChatKit SSE vs WebSocket

**Decision**: ChatKit Server-Sent Events (SSE) via `openai-chatkit` Python SDK
**Rationale**: ChatKit UI component (frontend) expects the ChatKit SSE protocol. The `openai-chatkit` SDK handles protocol framing, thread management, and streaming — no custom streaming logic needed. WebSockets would require a separate protocol implementation with no benefit.
**Alternatives considered**: WebSockets (more complex, incompatible with ChatKit UI), plain JSON polling (no streaming, poor UX)

---

## Decision 2: Backend store — ChatKit PostgresStore vs bridge to existing Conversation/Message tables

**Decision**: Dedicated ChatKit PostgresStore with two new tables (`chatkit_threads`, `chatkit_items`)
**Rationale**: The ChatKit store API uses JSONB-format thread items that don't map cleanly to our existing `Conversation`/`Message` schema (which uses plain string `content` and is designed for the stateless `/api/{user_id}/chat` endpoint). Bridging would require a custom Store adapter with complex data transformation. Dedicated tables are simpler and keep the two endpoints fully independent.
**Alternatives considered**: Custom Store adapter wrapping existing Conversation/Message tables (complex, tight coupling), InMemoryStore (loses history on restart — violates constitution VIII)

---

## Decision 3: Agent integration — call run_todo_agent() directly vs ChatKit Runner

**Decision**: Use `chatkit.agents.Runner.run_streamed()` with adapted tools — NOT calling `run_todo_agent()` directly
**Rationale**: `run_todo_agent()` uses non-streaming `Runner.run()` and returns a tuple — it cannot yield ChatKit stream events. The ChatKit SDK provides `stream_agent_response()` which converts streamed agent output into ChatKit's SSE event format. We reuse the same 5 `FunctionTool` wrappers (`_add_task_tool` etc.) from `todo_agent.py` but adapt the context from `TodoContext` to `ChatKitRequestContext`.
**Alternatives considered**: Add streaming to `run_todo_agent()` (would break existing interface and tests), create a completely separate agent (code duplication)

---

## Decision 4: Auth in ChatKit endpoint — JWT extraction method

**Decision**: Reuse existing `get_current_user` FastAPI dependency (extracts user_id from Bearer JWT)
**Rationale**: The `get_current_user` dependency already handles Better Auth JWT JWKS verification. The `/chatkit` endpoint uses the same `Depends(get_current_user)` pattern as `/api/{user_id}/chat`. The JWT token is stored in localStorage as `better_auth_jwt` and set as `Authorization: Bearer <token>` header by the frontend ChatKit UI.
**Alternatives considered**: Session cookie (Better Auth also supports this but the JWT pattern is already established), custom header (development only, insecure)

---

## Decision 5: DB session injection into ChatKit context

**Decision**: Inject SQLModel `Session` via FastAPI `Depends(get_session)` and pass in `ChatKitRequestContext` dataclass
**Rationale**: ChatKit server's `respond()` method receives a typed `context` parameter. By defining `ChatKitRequestContext(user_id, session)` and building it in the endpoint handler from FastAPI dependencies, we get the same session management guarantees as the rest of the API — proper cleanup, test overrides, etc.
**Alternatives considered**: Module-level session factory (bypasses FastAPI DI, harder to test), async session (requires async engine refactor)

---

## Decision 6: Frontend route and ChatKit UI integration

**Decision**: New page at `app/dashboard/chat/page.tsx` with ChatKit UI component, added to dashboard sidebar nav
**Rationale**: Dashboard is the authenticated area of the app. Adding a `/dashboard/chat` route follows the existing pattern (`/dashboard/todos`, `/dashboard/overview`). ChatKit UI component is configured with `api: { url: "/api/chatkit" }` and `getToken()` returning the Bearer JWT from localStorage.
**Alternatives considered**: Floating chat widget (harder to test, obscures existing UI), separate `/chat` route outside dashboard (requires separate auth guard)

---

## Key Technical Findings

### ChatKit Python SDK — verified patterns

```python
# Backend deps
pip install openai-chatkit psycopg[binary]

# Core server pattern
from chatkit.server import ChatKitServer, StreamingResult
from chatkit.agents import Runner, simple_to_agent_input, stream_agent_response, AgentContext
from chatkit.store import Store

# FastAPI endpoint pattern
@app.post("/chatkit")
async def endpoint(request: Request, user_id = Depends(get_current_user), session = Depends(get_session)):
    ctx = ChatKitRequestContext(user_id=user_id, session=session)
    result = await server.process(await request.body(), ctx)
    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    return Response(content=result.json, media_type="application/json")
```

### Better Auth JWT — verified from codebase

- Token stored at `localStorage.getItem("better_auth_jwt")`
- Frontend helper: `getJwtToken()` from `lib/auth-client.ts`
- Existing `get_current_user` dependency handles JWKS verification
- JWT `sub` claim = user_id

### Frontend ChatKit UI — assumed pattern

```typescript
// npm install @openai/chatkit  (package name to verify at implementation)
import { ChatKit } from "@openai/chatkit"

<ChatKit
  api={{
    url: process.env.NEXT_PUBLIC_BACKEND_URL + "/chatkit",
    headers: { Authorization: `Bearer ${getJwtToken()}` }
  }}
/>
```

### New DB tables required

```sql
-- chatkit_threads (ChatKit protocol table)
CREATE TABLE chatkit_threads (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    data JSONB NOT NULL
);
-- chatkit_items (ChatKit protocol table)
CREATE TABLE chatkit_items (
    id TEXT PRIMARY KEY,
    thread_id TEXT NOT NULL REFERENCES chatkit_threads(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    data JSONB NOT NULL
);
```

---

## Constitution Compliance Check

| Principle | Status | Notes |
|-----------|--------|-------|
| I. TDD | ✅ COMPLIANT | Tests before implementation required |
| VIII. Persistent Storage | ✅ COMPLIANT | PostgresStore + 2 new tables |
| IX. API Architecture + Stateless | ✅ COMPLIANT | ChatKit endpoint is stateless — loads thread from DB per request |
| X. Security + User Isolation | ✅ COMPLIANT | PostgresStore filters by user_id on all queries |
| XI. JWT Auth | ✅ COMPLIANT | Reuses `get_current_user` dependency |
| XII. MCP Architecture | ✅ COMPLIANT | Agent still calls MCP tools; ChatKit is the UI layer only |
| XIV. Performance | ✅ COMPLIANT | SSE streaming means first token < 2s; ChatKit is async |
