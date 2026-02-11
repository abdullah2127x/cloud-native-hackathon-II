---
name: openai-agents-sdk
description: |
  Builder and Guide for creating AI agents using the OpenAI Agents SDK (Python). Covers the full progression from a hello world agent to production-grade multi-agent systems with tools, handoffs, guardrails, streaming, structured outputs, MCP integration, and tracing.
  This skill should be used when building any agent with the OpenAI Agents SDK — whether creating a first agent, adding function tools, wiring multi-agent handoffs, implementing guardrails, integrating MCP servers, or hardening agents for production. Detects existing project structure before generating code.
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
---

# OpenAI Agents SDK

**Builder + Guide** for AI agents using `openai-agents` (Python).

## What This Skill Does

- Builds agents from hello world → multi-agent orchestration → production
- Generates `function_tool` functions, typed context, structured outputs
- Creates handoff chains (triage → specialist) and orchestrator-as-tools patterns
- Implements input/output/tool-level guardrails with tripwires
- Wires MCP server connections (stdio, HTTP)
- Configures tracing, RunConfig, and production env setup
- Detects existing agents/tools before generating

## What This Skill Does NOT Do

- Build the frontend UI (separate concern)
- Manage OpenAI API billing or rate limits
- Deploy to specific cloud platforms (generates runnable code only)
- Create realtime voice agents (use `RealtimeAgent` variant — see `references/advanced.md`)

---

## Before Implementation

| Source | What to Look For |
|--------|-----------------|
| **Codebase** | Existing `Agent(...)` definitions, `@function_tool` functions, `Runner` calls, context dataclasses |
| **Conversation** | Build level, agent purpose, tools needed, multi-agent topology, guardrail requirements |
| **Skill References** | Patterns from `references/` — authoritative source for all API usage |
| **User Guidelines** | Naming conventions, file structure, env var naming |

**Key files to read before starting:**
```
agents/           ← existing agent definitions
tools/            ← existing function tools
main.py / app.py  ← existing runner calls
.env / .env.example ← env var conventions
```

Only ask user for THEIR requirements. All SDK knowledge is in `references/`.

---

## Build Levels

```
Level 1 — Hello World
  └── Single Agent + Runner.run_sync()
  └── Plain text output

Level 2 — Agent with Tools          ← DEFAULT
  └── @function_tool decorated functions
  └── Typed RunContextWrapper[TContext]
  └── Structured output_type (Pydantic)
  └── Runner.run() / run_streamed()

Level 3 — Multi-Agent Orchestration
  └── Triage agent with handoffs=[]
  └── Orchestrator with agents as tools (.as_tool())
  └── RunConfig (model override, guardrails)

Level 4 — Production
  └── Input / output guardrails + tripwires
  └── Tool-level guardrails
  └── MCP server connections
  └── Tracing configuration
  └── Error handling, env vars, max_turns

Level 5 — Custom LLM Providers (Optional)
  └── Gemini via AsyncOpenAI + OpenAIChatCompletionsModel
  └── OpenRouter (any model: Claude, Llama, Gemini, GPT)
  └── LiteLLM unified wrapper
  └── load_dotenv() + os.getenv() for env vars
  └── RunConfig(tracing_disabled=True) for non-OpenAI
```

**Decision:** "Simple agent" → L2. "Route between agents" → L3. "Safety / MCP / tracing" → L4. "Not using OpenAI API" → L5.

---

## Workflow

### Step 1: Detect Project Type & Install

First, inspect the codebase to determine the package manager and whether `openai-agents` is already installed:

```bash
# 1. Check for uv project markers
ls pyproject.toml uv.lock 2>/dev/null

# 2. Check if openai-agents is already installed
pip show openai-agents 2>/dev/null || uv pip show openai-agents 2>/dev/null
```

Also check `pyproject.toml` and `requirements.txt` for existing declarations:
```
pyproject.toml       ← look for openai-agents in [project.dependencies] or [tool.uv.dev-dependencies]
requirements.txt     ← look for openai-agents line
uv.lock              ← presence confirms uv project
```

**Decision table:**

| Condition | Action |
|-----------|--------|
| `uv.lock` exists AND `openai-agents` NOT in deps | `uv add openai-agents` |
| `uv.lock` exists AND needs MCP support | `uv add "openai-agents[mcp]"` |
| `uv.lock` exists AND already installed | Skip — already available |
| No `uv.lock`, no `pyproject.toml` | `pip install openai-agents` |
| No `uv.lock`, needs MCP support | `pip install "openai-agents[mcp]"` |
| Already in `requirements.txt` or `pyproject.toml` | Skip install, verify with `pip show openai-agents` |

```bash
# uv project (uv.lock present)
uv add openai-agents python-dotenv
uv add "openai-agents[mcp]"        # if MCP servers needed

# standard pip project
pip install openai-agents python-dotenv
pip install "openai-agents[mcp]"   # if MCP servers needed
```

**Check for `.env` / `.env.example`:** Copy `assets/.env.example` to `.env` and fill in the API key for your provider:

```bash
# OpenAI (default)
OPENAI_API_KEY=sk-proj-...

# Gemini
GEMINI_API_KEY=...

# OpenRouter
OPENROUTER_API_KEY=...
```

### Step 2: Choose Pattern (see Decision Tree below)

### Step 3: Generate Code

**Level 1 — Hello World**
```python
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model="gpt-4o-mini",
)

result = Runner.run_sync(agent, "Hello!")
print(result.final_output)
```

**Level 2 — Agent with Tools** (see `references/core-agents.md`)
- Define `@function_tool` async functions with typed params + docstring
- Define context dataclass, pass to `Runner.run(agent, input, context=ctx)`
- Set `output_type=MyPydanticModel` for structured output

**Level 3 — Multi-Agent** (see `references/multi-agent.md`)
- Triage: `Agent(handoffs=[agent_a, agent_b])`
- Orchestrator: `Agent(tools=[agent_a.as_tool(...), agent_b.as_tool(...)])`

**Level 4 — Production** (see `references/guardrails.md`, `references/mcp-tracing.md`)

### Step 4: Run

```python
# Synchronous
result = Runner.run_sync(agent, "input")
print(result.final_output)

# Async
result = await Runner.run(agent, "input", context=ctx)

# Streaming
result = Runner.run_streamed(agent, "input")
async for event in result.stream_events():
    if event.type == "run_item_stream_event":
        if event.item.type == "message_output_item":
            print(ItemHelpers.text_message_output(event.item))
```

---

## Decision Tree

```
Using OpenAI API?
  ├── Yes → Start with Level 1–4 (OPENAI_API_KEY in .env)
  └── No  → Level 5 (Custom Provider)
      ├── Gemini? → AsyncOpenAI(base_url=GEMINI_URL) + OpenAIChatCompletionsModel
      ├── OpenRouter? → AsyncOpenAI(base_url=OPENROUTER_URL) + OpenAIChatCompletionsModel
      └── Multi-provider? → LiteLLM wrapper

Need a single agent?
  ├── No tools needed → Level 1
  └── Tools needed → Level 2
      ├── Multiple specialized agents?
      │   ├── Route by intent → Triage (handoffs) → Level 3
      │   └── Call all/some → Orchestrator (as_tool) → Level 3
      └── Safety/compliance needed → add Guardrails → Level 4
          └── External tools/APIs → add MCP → Level 4
```

---

## Key Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| `Runner.run_sync()` in async code | Use `await Runner.run()` in async context |
| `output_type` without Pydantic `BaseModel` | Use Pydantic models; plain dicts not supported |
| Catching all exceptions silently | Handle `InputGuardrailTripwireTriggered`, `OutputGuardrailTripwireTriggered` separately |
| Hardcoding `OPENAI_API_KEY` | Use `os.environ["OPENAI_API_KEY"]` |
| Not closing MCP server connections | Use `async with MCPServer...` context manager |
| Missing docstring on `@function_tool` | Docstring becomes the tool description sent to LLM |
| Passing context to LLM | Context is local only — never sent to model |
| Unbounded `max_turns` | Always set `max_turns` in production to prevent runaway loops |
| Using non-OpenAI provider without disabling tracing | Built-in tracing only works with OpenAI; use `RunConfig(tracing_disabled=True)` |
| Calling `os.getenv()` before `load_dotenv()` | Always call `load_dotenv()` first at module top level |

---

## Best Practices

| Practice | Why |
|----------|-----|
| **Direct Integration over LiteLLM** | Use AsyncOpenAI + OpenAIChatCompletionsModel; avoids quota issues, clearer control |
| **Always pass RunConfig for non-OpenAI** | Ensures model/provider/tracing settings apply to Runner.run() |
| **Cache MCP tool lists** | Use `cache_tools_list=True` on MCPServer to avoid re-fetching every turn |
| **Use handoffs for specialization** | Create separate agents per domain; route with triage agent |
| **Enable usage tracking** | Set `include_usage=True` in ModelSettings to monitor token/cost |
| **Disable tracing for non-OpenAI** | Built-in tracing only works with OpenAI; set `tracing_disabled=True` |
| **Handle errors gracefully** | Catch `AgentError`, `InputGuardrailTripwireTriggered`, `OutputGuardrailTripwireTriggered` |
| **Use streaming for UX** | Implement Runner.run_streamed() for real-time responses to users |
| **Share RunConfig across handoffs** | All agents in a handoff chain must use same RunConfig for consistent behavior |

---

## Error Handling

Catch SDK-specific exceptions:

```python
from agents import Runner, AgentError
from agents import InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered

try:
    result = await Runner.run(agent, "Hello", max_turns=10)
    print(result.final_output)
except InputGuardrailTripwireTriggered as e:
    print(f"Input blocked by guardrail: {e.output}")
except OutputGuardrailTripwireTriggered as e:
    print(f"Output blocked by guardrail: {e.output}")
except AgentError as e:
    print(f"Agent execution error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Troubleshooting

### Quota Exceeded Error on First Request

**Problem**: Getting quota exceeded when using LiteLLM or direct Gemini.

**Solution**: Switch to direct AsyncOpenAI integration (see `references/custom-llm-providers.md`):

```python
from agents import AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=client)
config = RunConfig(model=model, model_provider=client, tracing_disabled=True)
result = await Runner.run(agent, "Hello", run_config=config)
```

### MCP Server Connection Fails

- **Verify server is running**: Check port/URL is accessible
- **Set timeout**: Add `timeout=30` to MCPServerStreamableHttp params
- **Enable caching**: Use `cache_tools_list=True` to reduce handshakes
- **Check headers**: If auth required, pass `headers={"Authorization": "Bearer TOKEN"}`

### Gemini/OpenRouter API Errors

| Error | Check | Solution |
|-------|-------|----------|
| "Invalid API key" | `GEMINI_API_KEY` or `OPENROUTER_API_KEY` env var | Verify key is not wrapped in quotes; call `load_dotenv()` first |
| "Model not found" | Model name in base_url endpoint | Gemini: `gemini-2.5-flash`, `gemini-2.0-flash`; OpenRouter: check `https://openrouter.ai/docs/models` |
| "Bad request" | base_url format | Gemini: `https://generativelanguage.googleapis.com/v1beta/openai/`; OpenRouter: `https://openrouter.ai/api/v1` |
| "Timeout" | Network or server down | Add `timeout=Timeout(30)` to AsyncOpenAI; check provider status page |

### Agent Ignoring Model Configuration

**Problem**: Agent uses default OpenAI model even though you set custom model.

**Solution**: Always pass `run_config` to Runner.run():

```python
# ❌ Wrong — ignores your model
result = await Runner.run(agent, "Hello")

# ✅ Correct — applies your RunConfig
result = await Runner.run(agent, "Hello", run_config=config)
```

### Tracing Errors with Non-OpenAI Providers

**Problem**: "Tracing not supported" or "Invalid trace credentials" when using Gemini/OpenRouter.

**Solution**: Disable tracing in RunConfig:

```python
config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True  # ← Required for non-OpenAI
)
```

---

## Reference Files

| File | When to Read |
|------|---|
| `references/core-agents.md` | Agent config, function_tool, context, structured output, Runner methods |
| `references/multi-agent.md` | Handoffs, triage pattern, agents-as-tools, RunConfig |
| `references/guardrails.md` | Input/output guardrails, tool guardrails, tripwires |
| `references/mcp-tracing.md` | MCP servers (stdio/HTTP/manager), tracing, RunConfig advanced |
| `references/streaming.md` | Streaming event types, token streaming, progress patterns |
| `references/custom-llm-providers.md` | Gemini, OpenRouter, LiteLLM setup; RunConfig provider switching; env var best practices |

## Templates

Copy-paste starters in `assets/`:

| File | Use For |
|------|---------|
| `assets/agent_gemini.py` | Gemini-backed agent with tools |
| `assets/agent_openrouter.py` | OpenRouter agent (swap model in one line) |
| `assets/.env.example` | Copy to `.env` and fill keys |
