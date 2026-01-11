---
id: 0001
title: Create Next.js 16 App Router skill
stage: general
date: 2026-01-11
surface: skill-creation
model: Claude Sonnet 4.5
feature: none
branch: constitution
user: AbdullahQureshi
command: skill-creator-pro
labels: [skill, nextjs, app-router, server-components, server-actions, react19]
links:
  spec:
  ticket:
  adr:
  pr:
files:
  - .claude/skills/nextjs-16-app-router/SKILL.md
  - .claude/skills/nextjs-16-app-router/references/examples.md
  - .claude/skills/nextjs-16-app-router/references/best-practices.md
tests:
  - type: manual
    status: passed
    description: Skill files created and validated
---

## Prompt

Create a skill for Next.js 16 App Router with the following requirements:
- Auto-invoke when working with Next.js 16 App Router, Server Components, Server Actions, or React 19 features
- Use when creating routes, components, or API endpoints in Next.js
- Include Next.js 16 App Router file structure (app/ directory)
- Cover Server Components vs Client Components ('use client')
- Include Server Actions best practices
- Include Data fetching patterns (native fetch, no useEffect)
- Include Route handlers (route.ts for API routes)
- Include Metadata API usage
- Include Error handling (error.tsx, not-found.tsx)
- Include Loading states (loading.tsx)
- Include Common patterns for forms with Server Actions

## Response snapshot

Created a comprehensive Next.js 16 App Router skill with:
- Complete file structure documentation for app directory
- Clear distinction between Server Components and Client Components
- Best practices for Server Actions with validation and authentication
- Data fetching patterns using native fetch with different cache strategies
- Route handler examples for API endpoints
- Metadata API usage for SEO and dynamic metadata
- Error handling patterns with error.tsx and not-found.tsx
- Loading state implementations
- Form patterns with Server Actions
- Additional examples and best practices in references

## Outcome

- ✅ Impact: Next.js 16 App Router skill created with comprehensive documentation
- 🧪 Tests: Manual validation passed
- 📁 Files: 3 files created in .claude/skills/nextjs-16-app-router/
- 🔁 Next prompts: None needed
- 🧠 Reflection: Successfully created a production-ready skill with embedded domain expertise

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
