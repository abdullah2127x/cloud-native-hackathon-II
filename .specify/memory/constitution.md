# Todo In-Memory Console App Constitution
<!-- Constitution for Hackathon II Phase I: Todo In-Memory Python Console App -->

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
All implementation must be based on written specifications; No code may be written without an approved specification; Specifications must be refined until Claude Code generates correct output.
<!-- Implementation follows specifications, not ad-hoc development -->

### II. No Manual Coding Rule
All code must be generated via Claude Code based on specifications; No hand-written code is permitted; Any deviation violates the constitution.
<!-- Strict adherence to AI-assisted development methodology -->

### III. Phase 1 Scope Boundaries
Implementation limited to Phase 1 requirements only; No features from future phases may be implemented until constitution is updated; Console-only interface with in-memory storage.
<!-- Clear scope limitations prevent feature creep -->

### IV. In-Memory Storage Constraint
All data must remain in memory during application runtime; No persistent storage, databases, or file I/O allowed in Phase 1; Data loss on application exit is expected behavior.
<!-- Technology constraint specific to Phase 1 requirements -->

### V. Basic CRUD Operations Only
Must implement exactly 5 core operations: Add, Delete, Update, View, Mark Complete; No advanced features like priorities, tags, due dates, or recurring tasks.
<!-- Feature completeness boundary for Phase 1 -->

### VI. Clean Python Code Standards
All code must follow Python best practices and PEP 8 guidelines; Proper error handling and user feedback required; Clear, maintainable code structure mandated.
<!-- Quality standards for implementation -->

## Technology Stack Requirements
<!-- Additional Constraints, Technology Requirements, etc. -->

Python 3.13+ with UV package manager required; Claude Code and Spec-Kit Plus tools mandatory; Console interface only - no web UI or frontend development.
<!-- Technology stack boundaries and requirements -->

## Development Workflow
<!-- Development Process, Review Process, Quality Gates, etc. -->

Specifications must be written before implementation; Claude Code must generate all code based on specs; All changes must comply with constitution principles; Regular verification that no manual coding occurred.
<!-- Process requirements for development workflow -->

## Governance
<!-- Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

This constitution governs all development activities for Phase 1; Amendments require explicit update to constitution file; All PRs/reviews must verify compliance with these principles; Deviations require constitution update before implementation.
<!-- Governance and compliance requirements -->

**Version**: 1.0.0 | **Ratified**: 2026-01-05 | **Last Amended**: 2026-01-05
<!-- Version: MAJOR.MINOR.PATCH | Ratified: YYYY-MM-DD | Last Amended: YYYY-MM-DD -->
