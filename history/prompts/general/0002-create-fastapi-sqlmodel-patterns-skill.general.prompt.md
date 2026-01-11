---
id: 0002
title: Create FastAPI SQLModel patterns skill
stage: general
date: 2026-01-11
surface: skill-creation
model: Claude Sonnet 4.5
feature: none
branch: constitution
user: AbdullahQureshi
command: skill-creator-pro
labels: [skill, fastapi, sqlmodel, pydantic, rest-api, database]
links:
  spec:
  ticket:
  adr:
  pr:
files:
  - .claude/skills/fastapi-sqlmodel-patterns/SKILL.md
  - .claude/skills/fastapi-sqlmodel-patterns/references/examples.md
  - .claude/skills/fastapi-sqlmodel-patterns/references/best-practices.md
tests:
  - type: manual
    status: passed
    description: Skill files created and validated
---

## Prompt

Create a skill for FastAPI SQLModel patterns with the following requirements:
- Auto-invoke when creating FastAPI endpoints, SQLModel database models, or Pydantic schemas
- Use when building REST APIs or defining database tables with FastAPI and SQLModel
- Include SQLModel model definition (Base, Create, Read, Update patterns)
- Include FastAPI endpoint structure with async/await
- Include Dependency injection for database sessions
- Include HTTPException for error responses
- Include Response models and status codes
- Include Input validation with Pydantic
- Include Database session management (get_session dependency)
- Include Query patterns with SQLModel select()

## Response snapshot

Created a comprehensive FastAPI SQLModel patterns skill with:
- Complete SQLModel model definition patterns (Base, Create, Read, Update models)
- FastAPI endpoint structure with proper async/await usage
- Dependency injection patterns for database sessions
- HTTPException usage for error responses with proper status codes
- Response models and appropriate status code usage
- Comprehensive input validation with Pydantic
- Database session management patterns with get_session dependency
- Query patterns with SQLModel select() including advanced queries
- Additional examples and best practices in references

## Outcome

- ✅ Impact: FastAPI SQLModel patterns skill created with comprehensive documentation
- 🧪 Tests: Manual validation passed
- 📁 Files: 3 files created in .claude/skills/fastapi-sqlmodel-patterns/
- 🔁 Next prompts: None needed
- 🧠 Reflection: Successfully created a production-ready skill with embedded domain expertise

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
