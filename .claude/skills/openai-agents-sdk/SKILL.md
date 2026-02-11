---
name: openai-agents-sdk
description: |
  Builder and Guide for creating AI agents using the OpenAI Agents SDK (Python).
  Covers the full progression from hello world agents to production-grade multi-agent systems
  with tools, handoffs, guardrails, MCP integration, streaming, error handling, and observability.
  This skill should be used when building any agent with the OpenAI Agents SDK — whether creating
  a first agent, adding function tools, wiring multi-agent handoffs, implementing guardrails,
  integrating MCP servers, or hardening agents for production.
  Detects existing project structure and patterns before generating code.
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
---

# OpenAI Agents SDK

**Builder + Guide** for AI agents using OpenAI Agents (Python). Based on official OpenAI documentation.

## What This Skill Does

- Builds agents from hello world → multi-agent orchestration → production-grade systems
- Generates `@function_tool` functions with automatic schema and validation
- Creates multi-agent topologies: handoffs, orchestrators, agent-as-tool patterns
- Implements input/output guardrails with tripwire validation
- Integrates MCP servers (stdio, HTTP, SSE, custom)
- Configures streaming (token-level, structured output, nested agents)
- Sets up observability, tracing, error handling, sessions
- Detects existing agents/tools/patterns before generating

## What This Skill Does NOT Do

- Build the frontend/UI (separate concern)
- Manage OpenAI API billing or rate limits
- Deploy to cloud platforms (generates runnable code only)
- Create realtime voice agents (separate Agent type, use realtimeagent-sdk instead)

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing agent definitions, tools, project structure, conventions |
| **Conversation** | User's specific use case, build level, agent topology, features needed |
| **Skill References** | Domain patterns from `references/` (official API, best practices, examples) |
| **User Guidelines** | Project constraints, team standards, preferred approaches |

Only ask user for THEIR specific requirements. All SDK knowledge is in this skill's references.

---

## Quick Start: 3 Steps

### Step 1: Choose Your Provider & Model

**ONE question**: Which LLM provider do you prefer?

| Provider | Model | Cost | Speed | Best For |
|----------|-------|------|-------|----------|
| **OpenAI API** (default) | `gpt-4o-mini` | $$ | Very Fast | Production, best quality |
| **Gemini** | `gemini-2.5-flash` | $ | Fast | Prototyping, cost-sensitive |
| **OpenRouter** | Free models | Free + $$ | Varies | Model flexibility, fallbacks |
| **LiteLLM** | 20+ providers | Varies | Varies | Multi-provider, enterprise |

**Templates available**: Copy from `assets/` and customize agent for your use case.

### Step 2: Install & Setup

```bash
# Install SDK
pip install openai-agents

# (Optional) MCP support
pip install openai-agents[mcp]

# Set API key
export OPENAI_API_KEY=sk-proj-...
# OR: export GEMINI_API_KEY=...
# OR: export OPENROUTER_API_KEY=...
```

### Step 3: Create Agent

Copy template from `assets/` matching your provider choice, then customize:

```python
from agents import Agent, Runner, function_tool

@function_tool
async def your_tool(param: str) -> str:
    """Tool description (shown to LLM)."""
    return f"Result: {param}"

agent = Agent(
    name="Your Agent Name",
    instructions="What should the agent do?",
    tools=[your_tool],
    model="gpt-4o-mini",  # Or your chosen model
)

# Run
result = await Runner.run(agent, "User input here")
print(result.final_output)
```

---

## Build Levels

Choose your complexity level:

```
Level 1 — Hello World (simplest)
  └── Single Agent + basic execution
  └── Plain text output
  └── Time to working agent: 5 minutes

Level 2 — Agent with Tools ← DEFAULT
  └── @function_tool decorated functions
  └── Structured output (Pydantic models)
  └── Type-safe validation
  └── Time to working agent: 15 minutes

Level 3 — Multi-Agent Orchestration
  └── Handoff patterns (peer-to-peer delegation)
  └── Orchestrator patterns (centralized routing)
  └── Agent-as-tool patterns (nested specialization)
  └── Time to working agent: 30 minutes

Level 4 — Production-Grade
  └── Input/output guardrails + tripwires
  └── Tool-level guardrails & error handling
  └── MCP server integration
  └── Sessions & persistent memory
  └── Streaming (token, structured output, nested)
  └── Tracing & observability
  └── Time to working agent: 1-2 hours
```

**Decision**: No tools? → L1. Tools needed? → L2. Route between agents? → L3. Safety/observability needed? → L4.

---

## Workflow

### Step 1: Understand the Scope

| Question | Answer → Path |
|----------|---|
| "Which provider?" | Copy `assets/agent_[provider].py` template |
| "What tools needed?" | Use `@function_tool` for each tool (see `references/tools.md`) |
| "Multiple agents?" | Use handoffs or orchestrator pattern (see `references/multi-agent.md`) |
| "Safety critical?" | Add guardrails (see `references/guardrails.md`) |
| "Need streaming?" | Add streaming config (see `references/streaming.md`) |
| "External APIs?" | Add MCP servers (see `references/mcp.md`) |
| "Need observability?" | Enable tracing (see `references/tracing.md`) |

### Step 2: Read Relevant References

- **No tools?** → `references/agents.md`
- **Adding tools?** → `references/tools.md`
- **Multi-agent?** → `references/multi-agent.md`
- **Safety/validation?** → `references/guardrails.md`
- **Persistent state?** → `references/sessions.md`
- **Structured outputs?** → `references/structured-output.md`
- **Real-time responses?** → `references/streaming.md`
- **External integrations?** → `references/mcp.md`
- **Error handling?** → `references/error-handling.md`
- **Observability?** → `references/tracing.md`
- **Advanced patterns?** → `references/advanced-patterns.md`
- **Provider setup?** → `references/providers.md`

### Step 3: Copy Template & Customize

**Minimal template:**
```python
from agents import Agent, Runner

agent = Agent(
    name="MyAgent",
    instructions="You are helpful.",
    model="gpt-4o-mini",
)

result = await Runner.run(agent, "Hi")
print(result.final_output)
```

**Add tools:**
```python
from agents import function_tool

@function_tool
async def get_weather(city: str) -> str:
    """Get weather for a city."""
    return "sunny"

agent = Agent(
    name="Weather Agent",
    instructions="Help users check weather.",
    tools=[get_weather],
    model="gpt-4o-mini",
)
```

**Add guardrails:**
```python
from agents import guardrails

@guardrails.input_guardrail
def check_input(context, input_text):
    if len(input_text) > 1000:
        raise guardrails.GuardrailTriggered("Input too long")
    return input_text

agent = Agent(..., input_guardrails=[check_input])
```

See templates in `assets/` for complete examples.

### Step 4: Run & Test

```python
# Synchronous
result = Runner.run_sync(agent, "input")

# Async (recommended)
result = await Runner.run(agent, "input")

# Streaming
async for event in Runner.run_streamed(agent, "input"):
    if event.type == "text":
        print(event.text, end="", flush=True)
```

---

## Core Concepts (Quick Reference)

**Agent**: LLM equipped with instructions and tools. It follows a loop: receive input → decide actions → call tools → process results → respond.

**Tools**: Functions agents can call. Five types:
- Function tools (your Python functions via `@function_tool`)
- Agents as tools (nested agents via `agent.as_tool()`)
- Hosted tools (OpenAI's WebSearch, CodeInterpreter, etc.)
- MCP servers (external via stdio/HTTP/SSE)
- Custom tools (implement Tool interface)

**Multi-Agent Patterns**:
- **Handoffs**: Peer agents delegate to each other (agent1 → agent2)
- **Orchestrator**: Central agent routes to specialists (router → [agent_a, agent_b, agent_c])
- **Agent-as-Tool**: Specialize without handoff overhead

**Guardrails**: Validation gates before/after agent execution. Tripwire when violated.

**Streaming**: Real-time token output (token, text, structured results) for responsive UI.

**MCP**: Model Context Protocol servers provide standardized tool interfaces (filesystem, git, custom APIs).

**Sessions**: Persistent memory maintaining agent state across runs.

**Tracing**: Built-in observability visualizing agent loops and tool calls.

---

## Common Patterns

### Hello World (L1)
```python
from agents import Agent, Runner

agent = Agent(name="Echo", instructions="Repeat what user says.", model="gpt-4o-mini")
result = await Runner.run(agent, "Hello!")
print(result.final_output)
```

### With Tools (L2)
```python
@function_tool
async def add(a: int, b: int) -> int:
    return a + b

agent = Agent(
    name="Calculator",
    instructions="Use add tool for math.",
    tools=[add],
    model="gpt-4o-mini",
)
result = await Runner.run(agent, "What is 2 + 3?")
```

### Multi-Agent Handoff (L3)
```python
math_agent = Agent(name="Math", instructions="Answer math questions.", model="gpt-4o-mini")
history_agent = Agent(name="History", instructions="Answer history questions.", model="gpt-4o-mini")
triage = Agent(
    name="Triage",
    instructions="Route to specialist.",
    handoffs=[math_agent, history_agent],
    model="gpt-4o-mini",
)
result = await Runner.run(triage, "What is 2+2?")  # Routes to math_agent
```

### With Guardrails (L4)
```python
@guardrails.input_guardrail
def check_length(context, input_text):
    if len(input_text) > 500:
        raise guardrails.GuardrailTriggered("Input exceeds 500 chars")
    return input_text

@guardrails.output_guardrail
def check_safety(context, output):
    if "unsafe" in output.lower():
        return "I can't respond to that."
    return output

agent = Agent(
    name="Safe",
    instructions="Be helpful and safe.",
    input_guardrails=[check_length],
    output_guardrails=[check_safety],
    model="gpt-4o-mini",
)
```

---

## Provider Support

All providers use same Agent API. Only setup differs:

| Provider | Env Var | Template | Model | Notes |
|----------|---------|----------|-------|-------|
| OpenAI | `OPENAI_API_KEY` | `assets/agent_openai.py` | `gpt-4o-mini` | Default, best quality |
| Gemini | `GEMINI_API_KEY` | `assets/agent_gemini.py` | `gemini-2.5-flash` | Cheapest |
| OpenRouter | `OPENROUTER_API_KEY` | `assets/agent_openrouter.py` | Free models | Most flexible |
| LiteLLM | Various | `assets/agent_litellm.py` | Any (20+ providers) | Multi-provider support |

See `references/providers.md` for complete setup guide.

---

## Anti-Patterns

| Anti-Pattern | Why Problematic | Fix |
|---|---|---|
| No docstrings on tools | LLM doesn't know what tool does | Always add clear docstring |
| `Runner.run_sync()` in async code | Blocks event loop | Use `await Runner.run()` instead |
| Ignoring guardrail tripwires | Silent failures | Catch `GuardrailTriggered` exception |
| Tools without error handling | Crashes stop agent | Use `failure_error_function` |
| Hardcoding API keys | Security risk | Use environment variables |
| No context typing | Type errors at runtime | Use `Agent[YourContextType]` |
| Large tool outputs | Context overflow | Return structured data, not raw text |
| Tools with side effects in prompts | LLM calls tools unnecessarily | Use `tool_choice="required"` to require explicit use |

---

## Observability

Enable tracing to visualize agent behavior:

```python
from agents import Tracer

tracer = Tracer()

async def main():
    result = await Runner.run(agent, "input", tracer=tracer)
    print(tracer.get_trace())  # Visualize in OpenAI Dashboard
```

Tracing shows: agent loops, tool calls, LLM reasoning, timing.

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/agents.md` | Agent basics, configuration, lifecycle, hooks |
| `references/tools.md` | Tool creation, validation, error handling, function_tool decorator |
| `references/multi-agent.md` | Handoffs, orchestrators, agent-as-tool patterns, routing logic |
| `references/guardrails.md` | Input/output validation, tripwires, custom checks |
| `references/streaming.md` | Token streaming, structured output streaming, event handling |
| `references/structured-output.md` | Pydantic models, TypedDict, output_type configuration |
| `references/mcp.md` | MCP servers (stdio, HTTP, SSE), configuration, error handling |
| `references/sessions.md` | Memory backends, persistence, session configuration |
| `references/error-handling.md` | Exception handling, failure functions, recovery |
| `references/tracing.md` | Observability, OpenAI Dashboard, custom tracing |
| `references/context.md` | Dependency injection, context typing, lifecycle |
| `references/advanced-patterns.md` | Dynamic instructions, custom hooks, lifecycle management |
| `references/providers.md` | Provider setup, API keys, model selection |

## Templates

Copy-paste starters matching your provider:

| File | Provider | Model | Base Level |
|------|----------|-------|-----------|
| `assets/agent_openai.py` | OpenAI | gpt-4o-mini | L2 (tools) |
| `assets/agent_gemini.py` | Gemini | gemini-2.5-flash | L2 (tools) |
| `assets/agent_openrouter.py` | OpenRouter | free-model | L2 (tools) |
| `assets/agent_litellm.py` | LiteLLM | gemini-2.5-flash | L2 (tools) |
| `assets/agent_l1_hello_world.py` | OpenAI | gpt-4o-mini | L1 (no tools) |
| `assets/agent_l3_handoff.py` | OpenAI | gpt-4o-mini | L3 (multi-agent) |
| `assets/agent_l4_production.py` | OpenAI | gpt-4o-mini | L4 (full features) |
| `assets/.env.example` | - | - | Configuration |

---

## Next Steps

1. **Read Step 1 workflow** (choose provider)
2. **Copy relevant template** from `assets/`
3. **Add API key** to `.env`
4. **Customize agent** (name, instructions, tools)
5. **Read reference** for the feature you need (tools, guardrails, etc.)
6. **Test locally** before deploying

---

## Sources

- [OpenAI Agents SDK Official Docs](https://openai.github.io/openai-agents-python/)
- [GitHub Repository](https://github.com/openai/openai-agents-python)
- [Official Examples](https://openai.github.io/openai-agents-python/examples/)
- [MCP Server Integration](https://openai.github.io/openai-agents-python/ref/mcp/server/)
- [Tools API Reference](https://openai.github.io/openai-agents-python/tools/)
