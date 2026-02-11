---
id: "0005"
title: Create ChatKit Server skill
stage: general
date: 2026-02-11T00:00:00Z
surface: project
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: AbdullahQureshi
command: /skill-creator-pro
labels: [skill, chatkit, fastapi, agent]
links:
  spec: none
  ticket: none
  adr: none
  pr: none
files:
  - .claude/skills/chatkit-server/SKILL.md
  - .claude/skills/chatkit-server/references/core-concepts.md
  - .claude/skills/chatkit-server/references/agent-patterns.md
  - .claude/skills/chatkit-server/references/store-implementations.md
  - .claude/skills/chatkit-server/references/tools-widgets.md
  - .claude/skills/chatkit-server/references/production.md
tests:
  - none
---

## Prompt

Using your "skill-creator-pro" skill create a new skill for ChatKit Server. I will use it to build conversational AI backends from hello world to professional production systems. Use context7 skill to study official documentation and then build it so no self assumed knowledge.

## Response snapshot

Created the `chatkit-server` skill using skill-creator-pro framework. Domain discovery was performed via Context7 across 5 high-reputation OpenAI sources (chatkit-python, openai-chatkit-advanced-samples, chatkit-js). User requirements gathered via AskUserQuestion: Both Builder+Guide, Python+FastAPI, Agent integration focus, codebase-aware.

Skill structure:
- SKILL.md: Build levels (L1 hello world → L2 agent → L3 production), decision tree, anti-patterns, workflow
- references/core-concepts.md: ChatKitServer, Store interface, RequestContext, threads/items
- references/agent-patterns.md: Full agent integration with streaming, thread history, tools
- references/store-implementations.md: InMemoryStore + full PostgreSQL Store with Neon support
- references/tools-widgets.md: @function_tool, ClientToolCall, progress events, Card/Image/Text widgets
- references/production.md: Auth patterns (JWT, Better Auth, custom header), CORS, env vars, error handling, security checklist

## Outcome

- ✅ Impact: New `chatkit-server` skill available immediately; covers hello world to production with zero self-assumed knowledge
- 🧪 Tests: Skill auto-detected and listed in system skills on next session
- 📁 Files: 6 files created under .claude/skills/chatkit-server/
- 🔁 Next prompts: Use `/chatkit-server` to build a ChatKit backend; run `/skill-validator` to score quality
- 🧠 Reflection: Context7 provided high-quality verified patterns. PostgreSQL store included full Neon-compatible connection string. Better Auth JWT pattern added as a variant for this project's auth system.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment: Run skill-validator to identify any gaps in coverage
