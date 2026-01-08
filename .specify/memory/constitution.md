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
- Type hints required
- Linting rules enforced
- Consistent formatting applied

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

JWT-based authentication is REQUIRED; Shared secret MUST secure frontend and backend communication; Token verification MUST occur before data access.

**Rationale**: Stateless authentication enables scalability.

### XII. Architecture

Monorepo structure is REQUIRED; Frontend and backend MUST be separated; Specifications MUST be shared between both.

**Rationale**: Single repository enables full context visibility and simplifies specification management.

---

## Technology Stack

**Frontend**: Next.js, TypeScript, Tailwind CSS, Better Auth

**Backend**: Python, FastAPI, SQLModel, Pydantic

**Database**: PostgreSQL (Neon Serverless)

**Development**: Claude Code, Spec-Kit Plus

**Rationale**: Technology stack is fixed.

---

**Version**: 2.0.0
**Ratified**: 2026-01-05
**Last Amended**: 2026-01-08

---

*This constitution is the single source of truth. All development MUST comply with these principles.*
