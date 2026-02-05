# Implementation Plan: MCP Server for Todo Operations

**Branch**: `001-mcp-todo-tools` | **Date**: 2026-02-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-mcp-todo-tools/spec.md`

## Summary

Build an MCP (Model Context Protocol) server that exposes 5 todo CRUD operation tools (add_task, list_tasks, complete_task, delete_task, update_task) for AI agents. The MCP server integrates with the existing FastAPI backend as a dependency/middleware, validates JWT tokens from tool invocation headers, enforces user isolation, and provides structured error responses. All tools operate statelessly with database transactions supporting automatic retry on failures.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Official MCP SDK (Python), FastAPI, SQLModel, Pydantic, Better Auth (JWT validation), existing database session management
**Storage**: Neon PostgreSQL (existing, reuse Task model and connection pooling)
**Testing**: pytest with database fixtures, unit tests for each tool handler, integration tests for MCP protocol compliance
**Target Platform**: FastAPI backend server (runs alongside existing REST API)
**Project Type**: Web backend extension (MCP server module within existing FastAPI monorepo backend)
**Performance Goals**: Tool response < 2s under normal load, 50 concurrent tool invocations without race conditions
**Constraints**:
- Must validate JWT tokens before tool execution
- All database queries must filter by user_id
- Structured JSON logging (error type, timestamp, user_id, tool, operation)
- Hard delete for delete_task (no soft delete)
- 1-2 retry attempts on transient database failures
**Scale/Scope**: 5 MCP tools, existing Task model (no new entities), integration with existing auth and database infrastructure

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles**:
- ✅ **I. Test-Driven Development**: Plan includes pytest tests for all 5 tools (unit + integration)
- ✅ **II. No Manual Coding**: All code will be generated via Claude Code from this plan and tasks
- ✅ **III. Code Quality Standards**:
  - Type safety: Python type hints with Pydantic models
  - Error handling: Structured responses for all error cases
  - Input validation: Pydantic schemas for all tool parameters
  - Test coverage: Minimum 70% required
  - No hardcoded credentials: JWT secret from environment variables
- ✅ **IV. Development Workflow**: Following Specify → Plan → Tasks → Implement
- ✅ **V. Governance**: This plan complies with constitution v3.0.0

**Project Scope & Boundaries**:
- ✅ **VI. Scope Boundaries**:
  - Phase 3 AI-powered chatbot scope
  - Only features in spec.md will be implemented
  - Stateless architecture for all MCP tool operations
  - Proper tool boundaries through MCP

**Technical Constraints**:
- ✅ **VIII. Persistent Storage**: Reuses existing Neon PostgreSQL database
- ✅ **IX. API Architecture**:
  - MCP tools provide structured interface for AI agent
  - Chat endpoint remains stateless (handled in separate spec)
  - Each request independent, fetches state from database
- ✅ **X. Security & User Isolation**:
  - Every tool validates user_id from JWT
  - All database queries filtered by authenticated user_id
  - Cross-user access prevented
- ✅ **XI. Authentication**:
  - JWT-based authentication required
  - JWT token validated before tool execution
  - User_id extracted from JWT claims
- ✅ **XII. Architecture**:
  - Monorepo structure maintained (backend/mcp/ module)
  - MCP Server is only interface between AI agent and application logic
  - AI agent does not directly access database
  - All task operations exposed as MCP tools
  - Each tool atomic and independently testable
- ✅ **XIII. MCP Tools Governance**:
  - All 5 tools are stateless functions
  - Each tool enforces user isolation via user_id validation
  - Tool parameters validated with Pydantic before execution
  - Consistent response format across all tools
  - Structured error messages returned
  - Tool design follows atomicity, isolation, idempotency, error transparency
- ✅ **XIV. Performance Requirements**:
  - AI agent response time < 5s (tool operations < 2s)
  - Database queries use existing indexes

**Technology Stack**:
- ✅ Backend: Python FastAPI with SQLModel, Pydantic (uv package manager)
- ✅ AI Layer: Official MCP SDK (Python)
- ✅ Database: Neon Serverless PostgreSQL (existing)
- ✅ Authentication: Better Auth with JWT tokens (existing)
- ✅ Development: Claude Code, Spec-Kit Plus

**Constitution Compliance**: ✅ PASSED - No violations detected

## Project Structure

### Documentation (this feature)

```text
specs/001-mcp-todo-tools/
├── spec.md              # Feature specification
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0: MCP SDK patterns, FastAPI middleware, JWT validation
├── data-model.md        # Phase 1: Tool schemas and response models
├── quickstart.md        # Phase 1: Developer setup and testing guide
├── contracts/           # Phase 1: MCP tool schemas (JSON format)
│   ├── add_task.json
│   ├── list_tasks.json
│   ├── complete_task.json
│   ├── delete_task.json
│   └── update_task.json
└── tasks.md             # Phase 2: NOT created by /sp.plan
```

### Source Code (repository root)

```text
backend/
├── mcp/                              # NEW: MCP server module
│   ├── __init__.py                   # MCP server initialization and registration
│   ├── server.py                     # Main MCP server class (FastAPI dependency)
│   ├── middleware.py                 # JWT validation middleware for tool invocations
│   ├── schemas.py                    # Pydantic schemas for tool parameters and responses
│   ├── tools/                        # Tool handler implementations
│   │   ├── __init__.py
│   │   ├── add_task.py               # add_task tool handler
│   │   ├── list_tasks.py             # list_tasks tool handler
│   │   ├── complete_task.py          # complete_task tool handler
│   │   ├── delete_task.py            # delete_task tool handler
│   │   └── update_task.py            # update_task tool handler
│   ├── auth.py                       # JWT validation and user_id extraction utilities
│   ├── errors.py                     # Error handling and structured error responses
│   └── logging_config.py             # Structured JSON logging configuration
├── src/
│   ├── models/                       # EXISTING: SQLModel Task model (reuse)
│   ├── database.py                   # EXISTING: Database session management (reuse)
│   └── main.py                       # MODIFIED: Register MCP server as FastAPI dependency
└── tests/
    └── mcp/                          # NEW: MCP server tests
        ├── __init__.py
        ├── conftest.py               # Pytest fixtures (mock JWT, database)
        ├── test_add_task.py          # Unit tests for add_task tool
        ├── test_list_tasks.py        # Unit tests for list_tasks tool
        ├── test_complete_task.py     # Unit tests for complete_task tool
        ├── test_delete_task.py       # Unit tests for delete_task tool
        ├── test_update_task.py       # Unit tests for update_task tool
        ├── test_auth.py              # Tests for JWT validation
        ├── test_errors.py            # Tests for error handling
        └── test_integration.py       # Integration tests (MCP protocol compliance)
```

**Structure Decision**: Web backend extension. The MCP server is implemented as a new module (`backend/mcp/`) within the existing FastAPI monorepo backend. This maintains the monorepo structure while cleanly separating MCP-specific logic from the existing REST API. The MCP server integrates as a FastAPI dependency/middleware, allowing it to intercept tool invocation requests and validate JWT tokens before execution.

## Complexity Tracking

No constitutional violations requiring justification.

