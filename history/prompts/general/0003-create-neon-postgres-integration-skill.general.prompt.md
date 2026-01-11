---
id: 0003
title: Create Neon Postgres integration skill
stage: general
date: 2026-01-11
surface: skill-creation
model: Claude Sonnet 4.5
feature: none
branch: constitution
user: AbdullahQureshi
command: skill-creator-pro
labels: [skill, neon, postgresql, database, connection, migrations, sqlmodel]
links:
  spec:
  ticket:
  adr:
  pr:
files:
  - .claude/skills/neon-postgres-integration/SKILL.md
  - .claude/skills/neon-postgres-integration/references/examples.md
  - .claude/skills/neon-postgres-integration/references/best-practices.md
tests:
  - type: manual
    status: passed
    description: Skill files created and validated
---

## Prompt

Create a skill for Neon Postgres integration with the following requirements:
- Auto-invoke when configuring Neon database connections, creating migrations, or writing database queries
- Use for connection setup and database operations with Neon Serverless PostgreSQL
- Include Neon connection string format
- Include SQLModel engine configuration
- Include Connection pooling with Neon
- Include Environment variable setup (DATABASE_URL)
- Include SSL requirements for Neon
- Include Migration strategy with Alembic
- Include Connection health checks
- Include Error handling for database operations

## Response snapshot

Created a comprehensive Neon Postgres Integration skill with:
- Complete Neon connection string format documentation
- SQLModel engine configuration optimized for Neon
- Connection pooling best practices with Neon-specific settings
- Environment variable setup patterns (DATABASE_URL)
- SSL requirements and configuration for Neon
- Migration strategy with Alembic for Neon PostgreSQL
- Connection health checks with multiple levels of validation
- Comprehensive error handling for database operations
- Additional examples and best practices in references

## Outcome

- ✅ Impact: Neon Postgres integration skill created with comprehensive documentation
- 🧪 Tests: Manual validation passed
- 📁 Files: 3 files created in .claude/skills/neon-postgres-integration/
- 🔁 Next prompts: None needed
- 🧠 Reflection: Successfully created a production-ready skill with embedded domain expertise

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
