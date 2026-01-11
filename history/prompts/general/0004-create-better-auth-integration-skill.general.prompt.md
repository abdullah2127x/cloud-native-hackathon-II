---
id: 0004
title: Create Better Auth integration skill
stage: general
date: 2026-01-11
surface: skill-creation
model: Claude Sonnet 4.5
feature: none
branch: constitution
user: AbdullahQureshi
command: skill-creator-pro
labels: [skill, better-auth, authentication, jwt, sessions, protected-routes]
links:
  spec:
  ticket:
  adr:
  pr:
files:
  - .claude/skills/better-auth-integration/SKILL.md
  - .claude/skills/better-auth-integration/references/examples.md
  - .claude/skills/better-auth-integration/references/best-practices.md
tests:
  - type: manual
    status: passed
    description: Skill files created and validated
---

## Prompt

Create a skill for Better Auth integration with the following requirements:
- Auto-invoke when implementing authentication, user sessions, JWT tokens, or protected routes
- Use for signup/signin flows and auth verification with Better Auth
- Include Better Auth setup in Next.js (lib/auth.ts)
- Include Email/password authentication config
- Include JWT token generation and verification
- Include Protected route patterns (middleware)
- Include Session management
- Include Frontend auth client usage
- Include Backend JWT validation in FastAPI
- Include Shared secret configuration (BETTER_AUTH_SECRET)
- Include Token refresh patterns

## Response snapshot

Created a comprehensive Better Auth Integration skill with:
- Complete Better Auth setup for Next.js (lib/auth.ts)
- Email/password authentication configuration
- JWT token generation and verification patterns
- Protected route patterns with middleware examples
- Session management strategies
- Frontend auth client usage examples
- Backend JWT validation in FastAPI
- Shared secret configuration (BETTER_AUTH_SECRET)
- Token refresh patterns and strategies
- Additional examples and best practices in references

## Outcome

- ✅ Impact: Better Auth integration skill created with comprehensive documentation
- 🧪 Tests: Manual validation passed
- 📁 Files: 3 files created in .claude/skills/better-auth-integration/
- 🔁 Next prompts: None needed
- 🧠 Reflection: Successfully created a production-ready skill with embedded domain expertise

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
