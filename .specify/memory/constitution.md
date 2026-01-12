<!--
SYNC IMPACT REPORT:
Version change: 2.0.0 → 2.1.0
Modified principles:
- Tech Stack (added specific version constraints)
- Code Quality (expanded with specific requirements)
- Architecture (added authentication and performance principles)
Added sections: Performance Requirements
Removed sections: None
Templates requiring updates:
- ✅ .specify/templates/plan-template.md
- ✅ .specify/templates/spec-template.md
- ✅ .specify/templates/tasks-template.md
- ✅ .specify/templates/commands/*.md
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

## Project Scope

### VI. Required Features

- Basic CRUD operations (Add, Delete, Update, View, Mark Complete) as web application
- User authentication
- Multi-user task isolation
- RESTful API
- Persistent database storage
- Responsive UI

### VII. Prohibited Features

- AI chatbot or natural language processing
- Advanced task features (priorities, tags, dates, recurring, reminders)
- Real-time collaboration
- Mobile native applications
- Container orchestration
- Event-driven architecture
- Voice commands

**Rationale**: Clear boundaries prevent scope creep.

---

## Technical Constraints

### VIII. Persistent Storage

Database storage is REQUIRED; In-memory storage is PROHIBITED; Data MUST persist across restarts.

**Rationale**: Multi-user applications require persistence.

### IX. RESTful API Architecture

Backend MUST expose RESTful API; Frontend MUST communicate via HTTP/HTTPS; JSON format required.

**Rationale**: Standard contract between frontend and backend.

### X. Security & User Isolation

Every user MUST only access their own data; User identity MUST be cryptographically verified; User identity MUST filter all data queries; Cross-user data access is PROHIBITED.

**Rationale**: Multi-user security requires strict isolation and verified identity.

### XI. Authentication

JWT-based authentication is REQUIRED; Shared secret MUST secure frontend and backend communication; Token verification MUST occur before data access; Better Auth with JWT tokens is REQUIRED.

**Rationale**: Stateless authentication enables scalability.

### XII. Architecture

Monorepo structure is REQUIRED; Frontend and backend MUST be separated; Specifications MUST be shared between both; Backend exposes REST API only; All database queries through SQLModel ORM; Environment variables for all secrets.

**Rationale**: Single repository enables full context visibility and simplifies specification management.

### XIII. Performance Requirements

API response time MUST be < 200ms; Database queries MUST be optimized with indexes; Frontend initial load MUST be < 2s.

**Rationale**: Performance requirements ensure responsive user experience.

---

## Technology Stack

**Frontend**: Next.js 16 App Router, TypeScript, Tailwind CSS, Better Auth

**Backend**: Python FastAPI with SQLModel, Pydantic, uv (Universal Python Package Installer)

**Database**: Neon Serverless PostgreSQL

**Authentication**: Better Auth with JWT tokens

**Deployment**: Vercel (frontend), separate backend

**Development**: Claude Code, Spec-Kit Plus, uv for Python dependency management

**Rationale**: Technology stack is fixed and MUST be followed as specified.

---

**Version**: 2.1.0
**Ratified**: 2026-01-05
**Last Amended**: 2026-01-11

---

*This constitution is the single source of truth. All development MUST comply with these principles.*