---
id: "0006"
title: Create OpenAI Agents SDK skill
stage: general
date: 2026-02-11T00:00:00Z
surface: project
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: AbdullahQureshi
command: /skill-creator-pro
labels: [skill, openai-agents, multi-agent, guardrails, mcp, streaming]
links:
  spec: none
  ticket: none
  adr: none
  pr: none
files:
  - .claude/skills/openai-agents-sdk/SKILL.md
  - .claude/skills/openai-agents-sdk/references/core-agents.md
  - .claude/skills/openai-agents-sdk/references/multi-agent.md
  - .claude/skills/openai-agents-sdk/references/guardrails.md
  - .claude/skills/openai-agents-sdk/references/mcp-tracing.md
  - .claude/skills/openai-agents-sdk/references/streaming.md
tests:
  - none
---

## Prompt

Using your skill "creator-skill-pro" create a new skill for OpenAI Agents SDK. I will use it to build AI agents from hello world to professional production systems. Use context7 skill to study official documentation and then build it so no self assumed knowledge.

## Response snapshot

Created the `openai-agents-sdk` skill using skill-creator-pro framework. Domain discovery via Context7 across 2 high-reputation sources: openai/openai-agents-python (benchmark 89.9, 406 snippets) and openai.github.io/openai-agents-python (3350 snippets). Queried 4 topic batches covering all user-selected feature areas. User requirements: Both Builder+Guide, all 4 feature areas (core, multi-agent, guardrails, MCP+production), codebase-aware.

Skill structure:
- SKILL.md: 4 build levels (L1 hello world → L2 tools → L3 multi-agent → L4 production), decision tree, anti-patterns, workflow
- references/core-agents.md: Agent config, @function_tool, RunContextWrapper, structured output, Runner methods, agent cloning
- references/multi-agent.md: Triage/handoffs, orchestrator/as_tool, Runner-inside-tool, RunConfig, pattern decision guide
- references/guardrails.md: Input/output guardrails with tripwires, tool-level guardrails, exception handling pattern
- references/mcp-tracing.md: stdio/HTTP/MCPServerManager, tracing config, custom processor, ModelSettings, custom providers
- references/streaming.md: Token streaming, item-level streaming, FastAPI SSE endpoint, ChatKit integration, RunResultStreaming

## Outcome

- ✅ Impact: New `openai-agents-sdk` skill available; covers hello world to production multi-agent systems with zero self-assumed knowledge
- 🧪 Tests: Skill auto-detected and listed in system skills on next session
- 📁 Files: 6 files created under .claude/skills/openai-agents-sdk/
- 🔁 Next prompts: Use `/openai-agents-sdk` to build agents; run `/skill-validator` to score quality
- 🧠 Reflection: Context7 benchmark 89.9 source provided very high-quality verified patterns. RunConfig documented completely from dataclass source. Both multi-agent patterns (handoffs vs as_tool) documented with clear decision guide.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment: Run skill-validator to identify gaps; consider adding OpenRouter/non-OpenAI provider patterns
