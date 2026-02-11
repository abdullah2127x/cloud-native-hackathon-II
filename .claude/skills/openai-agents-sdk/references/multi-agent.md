# OpenAI Agents SDK — Multi-Agent Orchestration

Source: openai/openai-agents-python (Context7, benchmark 89.9, High reputation)

---

## Two Multi-Agent Patterns

| Pattern | When to Use | Mechanism |
|---------|-------------|-----------|
| **Triage → Handoff** | Route to ONE specialist based on intent | `handoffs=[agent_a, agent_b]` |
| **Orchestrator → Tools** | Call MULTIPLE specialists, combine results | `agent.as_tool(...)` |

---

## Pattern 1: Triage with Handoffs

The triage agent inspects input and fully hands off to the appropriate specialist. Control does not return to triage.

```python
from agents import Agent, Runner
import asyncio

# Specialists
billing_agent = Agent(
    name="Billing Agent",
    instructions="Handle all billing questions: invoices, payments, refunds.",
    model="gpt-4o-mini",
)

technical_agent = Agent(
    name="Technical Agent",
    instructions="Handle all technical support: bugs, setup, errors.",
    model="gpt-4o-mini",
)

# Triage — routes to the right specialist
triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are a customer support router. "
        "For billing questions, hand off to Billing Agent. "
        "For technical issues, hand off to Technical Agent. "
        "For anything else, handle it yourself."
    ),
    handoffs=[billing_agent, technical_agent],
    model="gpt-4o-mini",
)

async def main():
    result = await Runner.run(triage_agent, "My invoice is wrong", max_turns=10)
    print(result.final_output)
    print(f"Handled by: {result.last_agent.name}")

asyncio.run(main())
```

### Handoff with Custom Filter

Control what history the receiving agent sees:

```python
from agents import Agent, handoff
from agents.run import RunConfig

def filter_sensitive(inputs):
    # Strip previous agent messages, pass only the last user message
    return [item for item in inputs if item.get("role") == "user"][-1:]

specialist = Agent(name="Specialist", instructions="...")

triage = Agent(
    name="Triage",
    instructions="Route to specialist when needed.",
    handoffs=[
        handoff(
            agent=specialist,
            input_filter=filter_sensitive,
            tool_name_override="escalate_to_specialist",
            tool_description_override="Escalate complex issues to specialist.",
        )
    ],
)
```

---

## Pattern 2: Orchestrator with Agents as Tools

The orchestrator calls sub-agents like tools and combines results. Control stays with orchestrator throughout.

```python
from agents import Agent, Runner
import asyncio

# Specialists (defined as pure agents)
spanish_agent = Agent(
    name="Spanish Translator",
    instructions="Translate the user's message to Spanish. Return only the translation.",
)

french_agent = Agent(
    name="French Translator",
    instructions="Translate the user's message to French. Return only the translation.",
)

summarizer_agent = Agent(
    name="Summarizer",
    instructions="Summarize the provided text in one sentence.",
)

# Orchestrator uses them as tools
orchestrator = Agent(
    name="Orchestrator",
    instructions=(
        "You coordinate translation and summarization tasks. "
        "Call the relevant tools based on what the user needs."
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate text to Spanish.",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate text to French.",
        ),
        summarizer_agent.as_tool(
            tool_name="summarize_text",
            tool_description="Summarize a block of text.",
        ),
    ],
    model="gpt-4o-mini",
)

async def main():
    result = await Runner.run(
        orchestrator,
        "Translate 'Good morning' to Spanish and French, then summarize both.",
        max_turns=15,
    )
    print(result.final_output)

asyncio.run(main())
```

---

## Advanced: Runner Inside a Tool

Full control over sub-agent execution (custom RunConfig, retries, max_turns):

```python
from agents import Agent, Runner, function_tool, RunContextWrapper
from agents.run import RunConfig
from dataclasses import dataclass

@dataclass
class AppContext:
    user_id: str

@function_tool
async def run_research_agent(
    wrapper: RunContextWrapper[AppContext],
    topic: str,
) -> str:
    """Research a topic in depth and return a detailed report."""
    research_agent = Agent(
        name="Researcher",
        instructions="Research the given topic thoroughly.",
        model="gpt-4o",
    )
    result = await Runner.run(
        research_agent,
        f"Research this topic: {topic}",
        max_turns=5,
        run_config=RunConfig(
            workflow_name="Research Sub-Task",
            trace_metadata={"user_id": wrapper.context.user_id},
        ),
    )
    return str(result.final_output)
```

---

## RunConfig — Global Run Settings

```python
from agents.run import RunConfig
from agents.model_settings import ModelSettings

run_config = RunConfig(
    # Model override (applies to ALL agents in the run)
    model="gpt-4o",
    model_settings=ModelSettings(temperature=0.3, max_tokens=2048),

    # Safety
    input_guardrails=[my_input_guardrail],
    output_guardrails=[my_output_guardrail],

    # Handoff behavior
    handoff_input_filter=lambda inputs: inputs[-5:],  # last 5 items only
    nest_handoff_history=True,                         # collapse history on handoff

    # Tracing
    workflow_name="Customer Support Workflow",
    group_id=session_id,                  # links traces across turns
    trace_metadata={"user_id": user_id},
    tracing_disabled=False,
    trace_include_sensitive_data=False,   # hide inputs/outputs in traces
)

result = await Runner.run(agent, input, run_config=run_config, max_turns=20)
```

---

## Choosing a Pattern: Quick Guide

```
User message arrives
    │
    ├── "Route to one of N specialists"?
    │       └── Triage with handoffs
    │           Agent(handoffs=[a, b, c])
    │
    ├── "Call multiple specialists and combine"?
    │       └── Orchestrator with as_tool()
    │           Agent(tools=[a.as_tool(), b.as_tool()])
    │
    └── "Run sub-agent with full config control"?
            └── Runner.run() inside @function_tool
```

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Triage agent not handing off | Make instructions explicit: "You MUST hand off to X for Y questions" |
| Orchestrator calling wrong sub-agent | Provide clear `tool_description` on `.as_tool()` |
| History growing too large | Use `handoff_input_filter` to trim context |
| Missing `max_turns` in multi-agent | Always set — handoff chains can loop |
| Sub-agent models too expensive | Use `gpt-4o-mini` for specialists, `gpt-4o` for orchestrator |
