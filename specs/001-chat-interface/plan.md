# Implementation Plan: OpenAI ChatKit Conversation Interface

**Branch**: `001-chat-interface` | **Date**: 2026-02-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-chat-interface/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a conversational chatbot interface using OpenAI ChatKit that allows authenticated users to manage their todos through natural language interactions. The feature includes: (1) ChatKit UI integration on a new `/chat` route, (2) conversation and message persistence using PostgreSQL with stateless server architecture, (3) JWT authentication and strict user isolation, (4) virtual scrolling for performance with 100+ messages, and (5) empathetic, actionable error handling. The implementation follows the monorepo structure with Next.js frontend and FastAPI backend, maintaining separation between chat interface (this spec), AI agent logic (separate spec), and MCP tools (separate spec).

## Technical Context

**Language/Version**: TypeScript (Next.js 16 frontend), Python 3.11+ (FastAPI backend)
**Primary Dependencies**:
- Frontend: Next.js 16 App Router, React 18+, OpenAI ChatKit (npm package), Better Auth, Tailwind CSS
- Backend: FastAPI, SQLModel, Pydantic, Better Auth (JWT verification)
**Storage**: Neon Serverless PostgreSQL (Conversation and Message tables)
**Testing**: Jest + React Testing Library (frontend), pytest (backend)
**Target Platform**: Web application (Vercel for frontend, separate backend hosting)
**Project Type**: Web (monorepo with /frontend and /backend separation)
**Performance Goals**:
- Chat interface loads in <2s (SC-001)
- API response <5s for message submission (SC-002)
- 95% of API requests complete within 3s (SC-007)
- Virtual scrolling handles 100+ messages without jank (SC-011)
**Constraints**:
- Stateless server: No in-memory conversation state
- User isolation: 0% cross-user data leakage (SC-006)
- Authentication: JWT tokens required for all chat endpoints
- Responsive: 320px-1920px+ viewports (SC-003)
**Scale/Scope**:
- 2 new database tables (Conversation, Message)
- 1 new frontend route (/chat page)
- 1 new backend endpoint (POST /api/{user_id}/chat)
- 4 prioritized user stories with 15 acceptance scenarios
- Virtual scrolling library integration for message rendering

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Review

| Principle | Requirement | Status | Evidence |
|-----------|-------------|--------|----------|
| **I. TDD** | All features use TDD; tests pass before completion | ✅ PASS | Plan includes test structure; frontend (Jest) and backend (pytest) |
| **II. No Manual Coding** | All code generated via Claude Code from specs | ✅ PASS | Spec-driven workflow: spec → plan → tasks → implement |
| **III. Code Quality** | Type safety, error handling, validation, 70% coverage | ✅ PASS | TypeScript strict mode (frontend), Python type hints (backend), Pydantic/Zod validation |
| **IV. Workflow** | Specify → Plan → Tasks → Implement | ✅ PASS | Currently in Plan phase after Specification |
| **V. Governance** | Compliance verification required | ✅ PASS | This Constitution Check section |
| **VI. Scope** | Phase 3 AI chatbot; stateless architecture; MCP boundaries | ✅ PASS | Chat interface only; excludes AI agent/MCP (separate specs); stateless design confirmed |
| **VIII. Storage** | Database required; data persists across restarts | ✅ PASS | Neon PostgreSQL for Conversation and Message tables |
| **IX. API Architecture** | RESTful API; stateless chat endpoint; MCP tools | ✅ PASS | POST /api/{user_id}/chat; stateless (no in-memory state); MCP integration out of scope (separate spec) |
| **X. Security & Isolation** | Users only access own data; cryptographically verified | ✅ PASS | JWT validation; user_id filtering; FR-011, FR-012, FR-013; SC-006 (0% leakage) |
| **XI. Authentication** | JWT-based; Better Auth required | ✅ PASS | Better Auth with JWT tokens; token verification before data access |
| **XII. Architecture** | Monorepo; frontend/backend separation; SQLModel ORM | ✅ PASS | /frontend and /backend structure; SQLModel for database; env vars for secrets |
| **XII. AI Architecture** | MCP boundary; AI agent doesn't access DB directly | ✅ PASS | This spec covers chat interface only; AI agent logic in separate spec |
| **XIII. MCP Tools** | Stateless; user isolation; validated parameters | ✅ DEFERRED | MCP tools implementation in separate spec (out of scope here) |
| **XIV. Performance** | API <200ms; DB indexed; frontend <2s; AI <5s | ✅ PASS | SC-001 through SC-011 define performance targets; virtual scrolling for optimization |

### Assessment

**Overall Status**: ✅ **APPROVED - All gates pass**

**Justification for Deferred Items**:
- MCP Tools (XIII): This specification focuses on chat interface (ChatKit integration, persistence, UI). MCP server implementation is explicitly excluded and documented in separate specification per scope boundaries.

**No violations requiring complexity tracking table.**

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Monorepo: Web application with frontend/backend separation

backend/
├── app/
│   ├── models/
│   │   ├── conversation.py        # NEW: Conversation SQLModel
│   │   └── message.py             # NEW: Message SQLModel
│   ├── routes/
│   │   └── chat.py                # NEW: POST /api/{user_id}/chat endpoint
│   ├── schemas/
│   │   └── chat.py                # NEW: Pydantic request/response schemas
│   └── middleware/
│       └── auth.py                # EXISTING: JWT verification (reuse)
├── tests/
│   ├── test_models_conversation.py   # NEW: Conversation model tests
│   ├── test_models_message.py        # NEW: Message model tests
│   └── test_routes_chat.py           # NEW: Chat endpoint tests
└── migrations/
    └── versions/
        └── XXXX_add_conversation_message_tables.py  # NEW: DB migration

frontend/
├── app/
│   ├── chat/
│   │   └── page.tsx               # NEW: Chat interface route
│   ├── components/
│   │   ├── chat/
│   │   │   ├── ChatContainer.tsx  # NEW: Main chat wrapper
│   │   │   ├── MessageList.tsx    # NEW: Virtual scrolling message list
│   │   │   └── ChatInput.tsx      # NEW: Message input component
│   │   └── navigation/
│   │       └── NavBar.tsx         # MODIFIED: Add chat link
│   ├── lib/
│   │   └── api/
│   │       └── chat.ts            # NEW: Chat API client functions
│   └── hooks/
│       ├── useChat.ts             # NEW: Chat state management hook
│       └── useConversationHistory.ts  # NEW: Conversation loading hook
├── __tests__/
│   ├── chat/
│   │   ├── ChatContainer.test.tsx   # NEW
│   │   ├── MessageList.test.tsx     # NEW
│   │   └── ChatInput.test.tsx       # NEW
│   └── hooks/
│       ├── useChat.test.ts          # NEW
│       └── useConversationHistory.test.ts  # NEW
└── public/
    └── (no changes for this feature)

specs/001-chat-interface/  (this directory)
├── plan.md                        # This file
├── research.md                    # Phase 0 output (next)
├── data-model.md                  # Phase 1 output
├── quickstart.md                  # Phase 1 output
├── contracts/                     # Phase 1 output
│   └── chat-api.yaml              # OpenAPI spec for chat endpoint
└── tasks.md                       # Phase 2 output (/sp.tasks command)
```

**Structure Decision**: Option 2 (Web application with frontend/backend) is correct for this monorepo. The feature adds:
- **Backend**: 2 new models (Conversation, Message), 1 new route (chat.py), 1 migration, Pydantic schemas
- **Frontend**: 1 new page (/chat), 3 new components, 2 new hooks, 1 API client module
- **Tests**: Full coverage for both frontend (Jest) and backend (pytest)
- All changes follow existing monorepo conventions and maintain separation of concerns

## Complexity Tracking

*No constitutional violations requiring justification. This section is empty.*
