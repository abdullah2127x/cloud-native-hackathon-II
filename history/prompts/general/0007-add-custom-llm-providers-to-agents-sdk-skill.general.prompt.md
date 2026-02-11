---
id: "0007"
title: Add custom LLM providers to agents SDK skill
stage: general
date: 2026-02-11T00:00:00Z
surface: project
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: AbdullahQureshi
command: manual
labels: [skill, openai-agents, gemini, openrouter, litellm, custom-providers]
links:
  spec: none
  ticket: none
  adr: none
  pr: none
files:
  - .claude/skills/openai-agents-sdk/SKILL.md
  - .claude/skills/openai-agents-sdk/references/custom-llm-providers.md
  - .claude/skills/openai-agents-sdk/assets/agent_gemini.py
  - .claude/skills/openai-agents-sdk/assets/agent_openrouter.py
  - .claude/skills/openai-agents-sdk/assets/.env.example
tests:
  - none
---

## Prompt

Analyze the learning-openai project at D:\AbdullahQureshi\workspace\desktop_18_8_25\learning-openai\code to understand global LLM configuration patterns, then update the openai-agents-sdk skill to support Gemini, OpenRouter, and LiteLLM providers. See env var best practices in the project before starting updates.

## Response snapshot

Analyzed 8 Python files in the learning-openai project. Identified 3 proven LLM configuration patterns:

1. **Gemini via OpenAI-compatible API** (global_level.py, async_way.py, context.py, agent_level.py, tools.py): AsyncOpenAI with base_url to Gemini endpoint + OpenAIChatCompletionsModel wrapper
2. **OpenRouter** (open_router.py): Same AsyncOpenAI + OpenAIChatCompletionsModel pattern, different base_url
3. **LiteLLM** (litellm.py): Direct LitellmModel(model="gemini/...", api_key=...) wrapper

Env var best practice: load_dotenv() first, then os.getenv("KEY_NAME"). Never hardcode keys.
RunConfig pattern: RunConfig(model=model, model_provider=client, tracing_disabled=True)

Updates to openai-agents-sdk skill:
- Added Level 5 (Custom LLM Providers) to Build Levels
- Added custom-providers branch to Decision Tree
- Added 2 new anti-patterns (tracing_disabled + load_dotenv ordering)
- Added env var setup section with .env.example reference to Step 1
- Added Templates section at bottom

New files created:
- references/custom-llm-providers.md: Full Gemini/OpenRouter/LiteLLM docs + RunConfig switching + common issues
- assets/agent_gemini.py: Copy-paste Gemini template with tools and RunConfig
- assets/agent_openrouter.py: Copy-paste OpenRouter template with model options commented
- assets/.env.example: All provider env vars with source URLs

## Outcome

- ✅ Impact: openai-agents-sdk skill now supports Gemini, OpenRouter, LiteLLM — not just OpenAI API
- 🧪 Tests: none
- 📁 Files: 4 new files created, SKILL.md updated (Level 5, Decision Tree, anti-patterns, install step)
- 🔁 Next prompts: Use `/openai-agents-sdk` with Gemini or OpenRouter project; run `/skill-validator` to score
- 🧠 Reflection: learning-openai uses load_dotenv() + os.getenv() consistently. RunConfig(tracing_disabled=True) is always needed for non-OpenAI providers. Both Gemini and OpenRouter share identical AsyncOpenAI + OpenAIChatCompletionsModel pattern.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Run skill-validator to identify remaining gaps
