---
id: 0005
title: Create RESTful API design skill
stage: general
date: 2026-01-11
surface: skill-creation
model: Claude Sonnet 4.5
feature: none
branch: constitution
user: AbdullahQureshi
command: skill-creator-pro
labels: [skill, restful-api, http-methods, status-codes, api-design]
links:
  spec:
  ticket:
  adr:
  pr:
files:
  - .claude/skills/restful-api-design/SKILL.md
  - .claude/skills/restful-api-design/references/examples.md
  - .claude/skills/restful-api-design/references/best-practices.md
tests:
  - type: manual
    status: passed
    description: Skill files created and validated
---

## Prompt

Create a skill for RESTful API design with the following requirements:
- Auto-invoke when designing REST API endpoints, defining HTTP methods, or structuring API responses
- Use for API architecture decisions and following RESTful principles
- Include Resource naming conventions (plural nouns)
- Include HTTP method usage (GET, POST, PUT, PATCH, DELETE)
- Include Status code meanings (200, 201, 400, 401, 404, 500)
- Include Response format structure (success, data, message)
- Include Pagination patterns (page, limit, total)
- Include Error response format
- Include API versioning approach
- Include Request/response examples

## Response snapshot

Created a comprehensive RESTful API Design skill with:
- Resource naming conventions (plural nouns) with examples
- HTTP method usage patterns (GET, POST, PUT, PATCH, DELETE)
- Status code meanings and appropriate usage
- Response format structure with success/data/message patterns
- Pagination patterns with page/limit/total examples
- Error response format with detailed examples
- API versioning approaches (URL, header, query parameter)
- Complete request/response examples for various operations
- Additional examples and best practices in references

## Outcome

- ✅ Impact: RESTful API design skill created with comprehensive documentation
- 🧪 Tests: Manual validation passed
- 📁 Files: 3 files created in .claude/skills/restful-api-design/
- 🔁 Next prompts: None needed
- 🧠 Reflection: Successfully created a production-ready skill with embedded domain expertise

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
