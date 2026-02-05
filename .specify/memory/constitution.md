<!--
SYNC IMPACT REPORT:
Version change: 2.2.1 → 3.0.0
Modified principles:
- Scope Boundaries (Phase 2 → Phase 3: AI-Powered Chatbot)
- API Architecture (added stateless principle and MCP tools)
- Architecture (added AI architecture constraints and MCP governance)
- Performance Requirements (added AI agent response time)
Added sections:
- MCP Tools Governance (Section XIII)
Modified sections:
- Technology Stack (added AI Layer: OpenAI Agents SDK, MCP SDK, ChatKit)
Templates requiring updates:
- ✅ .specify/templates/plan-template.md (no changes needed)
- ✅ .specify/templates/spec-template.md (no changes needed)
- ✅ .specify/templates/tasks-template.md (no changes needed)
Follow-up TODOs: None
-->

# Project Constitution

## Core Principles

### I. Test-Driven Development

All features and bug fixes MUST be implemented using Test-Driven Development; Tests MUST pass before code is considered complete.

**Rationale**: TDD ensures correctness, provides living documentation, and prevents regressions.

### II. No Manual Coding

All code MUST be generated via Claude Code based on specifications; Hand-written code is prohibited.

**Rationale**: Spec-Driven Development ensures consistency and traceability from requirements to implementation.

### III. Code Quality Standards

All code MUST follow language-specific best practices; Every file MUST reference the Task ID and Spec that authorized its creation.

**Standards**:
- Type safety: TypeScript strict mode, Python type hints
- Error handling on all API endpoints
- Input validation using Pydantic/Zod
- Test coverage minimum 70%
- No hardcoded credentials

**Rationale**: Quality and traceability are non-negotiable.

### IV. Development Workflow

Specifications MUST be written before implementation; Implementation MUST follow specifications; All changes MUST comply with constitutional principles.

**Required Workflow**: Specify → Plan → Tasks → Implement

**Rationale**: Spec-Driven Development prevents unplanned work and ensures requirements drive implementation.

### V. Governance

This constitution governs all development; Amendments require version bump; Compliance MUST be verified; Deviations require constitutional amendment before proceeding.

**Amendment Procedure**:
- MAJOR: Incompatible principle changes
- MINOR: New principles added
- PATCH: Clarifications only

**Rationale**: Constitutional governance ensures predictability and prevents scope creep.

---

## Project Scope & Boundaries

### VI. Scope Boundaries

Phase 3 scope is LIMITED to AI-powered conversational task management; Features beyond specification are PROHIBITED; All features MUST be documented in specification before implementation.

**Current Phase**: Phase 3 - AI-Powered Todo Chatbot

**Scope Constraints**:
- MUST implement only features defined in active specifications
- MUST NOT add features without specification approval
- MUST maintain focus on conversational task management operations
- MUST use stateless architecture for all AI interactions
- MUST implement proper tool boundaries through MCP

**Rationale**: Constitutional scope boundaries prevent feature creep while allowing specifications to evolve within defined limits.

---

## Technical Constraints

### VIII. Persistent Storage

Database storage is REQUIRED; In-memory storage is PROHIBITED; Data MUST persist across restarts.

**Rationale**: Multi-user applications require persistence.

### IX. API Architecture

Backend MUST expose RESTful API for traditional operations; Chat endpoint MUST be stateless; MCP tools MUST provide structured interface for AI agent; Frontend MUST communicate via HTTP/HTTPS; JSON format required for all API communication.

**Stateless Principle**: Every request MUST fetch all required state from database; Server MUST NOT cache conversation state in memory; Each request MUST be independent and complete.

**Rationale**: Standard contract between frontend and backend; Stateless design enables horizontal scaling.

### X. Security & User Isolation

Every user MUST only access their own data; User identity MUST be cryptographically verified; User identity MUST filter all data queries; Cross-user data access is PROHIBITED.

**Rationale**: Multi-user security requires strict isolation and verified identity.

### XI. Authentication

JWT-based authentication is REQUIRED; Shared secret MUST secure frontend and backend communication; Token verification MUST occur before data access; Better Auth with JWT tokens is REQUIRED.

**Rationale**: Stateless authentication enables scalability.

### XII. Architecture

Monorepo structure is REQUIRED; Frontend and backend MUST be separated; Specifications MUST be shared between both; Backend exposes REST API and chat endpoint; All database queries through SQLModel ORM; Environment variables for all secrets.

**AI Architecture Constraints**:
- MCP Server MUST be the only interface between AI agent and application logic
- AI agent MUST NOT directly access database
- All task operations MUST be exposed as MCP tools
- Chat endpoint MUST manage conversation persistence
- Conversation state MUST be stored in database (stateless server)
- Each MCP tool MUST be atomic and independently testable

**Rationale**: Single repository enables full context visibility; MCP boundary ensures clean separation of concerns; Stateless design enables horizontal scaling.

### XIII. MCP Tools Governance

All MCP tools MUST be stateless functions; Each tool MUST enforce user isolation via user_id; Tool parameters MUST be validated before execution; Tool responses MUST follow consistent format; Tools MUST return structured error messages.

**Tool Design Principles**:
- Atomicity: Each tool does exactly one operation
- Isolation: Every tool receives and validates user_id
- Idempotency: Repeated calls with same parameters produce same result (where applicable)
- Error transparency: Clear error messages for debugging

**Rationale**: Consistent tool design ensures AI agent reliability and system security.

### XIV. Performance Requirements

API response time MUST be < 200ms; Database queries MUST be optimized with indexes; Frontend initial load MUST be < 2s; AI agent response time MUST be < 5s.

**Rationale**: Performance requirements ensure responsive user experience including AI interactions.

---

## Technology Stack

**Frontend**: Next.js 16 App Router, TypeScript, Tailwind CSS, Better Auth, OpenAI ChatKit

**Backend**: Python FastAPI with SQLModel, Pydantic (using uv as the required package manager)

**AI Layer**: OpenAI Agents SDK, Official MCP SDK (Python)

**Database**: Neon Serverless PostgreSQL

**Authentication**: Better Auth with JWT tokens

**Deployment**: Vercel (frontend), separate backend

**Development**: Claude Code, Spec-Kit Plus

**AI Provider**: OpenAI API (via OpenRouter for cost optimization)

**Rationale**: Technology stack is fixed and MUST be followed as specified.

---

**Version**: 3.0.0
**Ratified**: 2026-01-05
**Last Amended**: 2026-02-04

---

*This constitution is the single source of truth. All development MUST comply with these principles.*