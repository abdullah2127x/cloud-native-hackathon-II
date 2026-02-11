# OpenAI Agents SDK — Tools & Function Decorators

Source: openai/openai-agents-python (Context7, benchmark 89.9, High reputation)

---

## Overview

Tools are Python functions that agents can call to take actions. The `@function_tool` decorator automatically:
- Extracts parameter types and docstring
- Generates JSON schema for LLM understanding
- Handles validation and error recovery

---

## Basic Function Tool

```python
from agents import function_tool

@function_tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"The weather in {city} is sunny."
```

**How LLM uses it:**
1. Sees function name, docstring, and parameter types
2. Decides when calling is appropriate
3. Extracts arguments from reasoning
4. Executes function
5. Feeds result back to agent

---

## Parameter Types & Validation

```python
from pydantic import BaseModel, Field

class WeatherRequest(BaseModel):
    city: str = Field(..., description="City name")
    units: str = Field(default="celsius", description="celsius or fahrenheit")

@function_tool
def get_weather(request: WeatherRequest) -> str:
    """Get weather for a city in specified units."""
    return f"{request.temperature}° {request.units} in {request.city}"
```

**Supported parameter types:**
- Primitives: `str`, `int`, `float`, `bool`
- Collections: `list[str]`, `dict[str, int]`
- Pydantic models: Custom structured input
- Optional: `str | None`, `Optional[int]`

---

## Return Types

| Return Type | Use Case | Example |
|-------------|----------|---------|
| `str` | Simple text response | `return "completed"`  |
| `dict` | Structured data | `return {"status": "ok", "count": 5}` |
| `BaseModel` (Pydantic) | Complex objects | `return WeatherData(...)` |
| `list` | Multiple items | `return [item1, item2]` |

**Best practice:** Use Pydantic models for complex returns (agent can extract fields).

```python
from pydantic import BaseModel

class QueryResult(BaseModel):
    total: int
    items: list[str]

@function_tool
def search(query: str) -> QueryResult:
    """Search for items matching query."""
    return QueryResult(total=2, items=["item1", "item2"])
```

---

## Tool Docstrings (Critical!)

Docstring is the ONLY thing LLM sees. Be descriptive:

```python
# ❌ Bad: LLM doesn't know what this does
@function_tool
def process(data: str) -> str:
    return data

# ✅ Good: LLM understands purpose and parameters
@function_tool
def process_csv(
    csv_data: str,
    delimiter: str = ",",
    skip_header: bool = True,
) -> str:
    """
    Process CSV data by parsing rows and applying transformations.

    Args:
        csv_data: Raw CSV text with rows separated by newlines
        delimiter: Character separating columns (default: comma)
        skip_header: Skip first row if True (default: True)

    Returns:
        Processed CSV as string with transformations applied
    """
    # implementation
```

---

## Error Handling in Tools

Agents handle errors gracefully. Return meaningful messages:

```python
@function_tool
def divide(a: float, b: float) -> str:
    """Divide two numbers."""
    if b == 0:
        return "Error: Cannot divide by zero"
    return str(a / b)
```

**Agents will:**
1. See the error message
2. Adjust reasoning
3. Try alternative approaches
4. OR explain the error to user

---

## Async Tools

For I/O-bound operations (API calls, database queries):

```python
import asyncio

@function_tool
async def fetch_user(user_id: int) -> str:
    """Fetch user details from database."""
    # Can use async/await for non-blocking I/O
    result = await some_async_operation(user_id)
    return json.dumps(result)
```

---

## Using Tools in Agents

```python
from agents import Agent, Runner

@function_tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@function_tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

agent = Agent(
    name="Calculator",
    instructions="Use tools to solve math problems.",
    tools=[add, multiply],  # Pass list of tool functions
    model="gpt-4o-mini",
)

result = await Runner.run(agent, "What is 5 + 3 × 2?")
print(result.final_output)
```

---

## Tool Discovery by LLM

Agent automatically:
- Extracts function name, docstring, parameter names and types
- Builds JSON schema
- Shows available tools to LLM
- LLM decides WHEN to call based on conversation

**Make function names self-documenting:**
```python
# ❌ Bad
@function_tool
def do_thing(x: str) -> str:
    """..."""

# ✅ Good
@function_tool
def search_knowledge_base(query: str) -> str:
    """..."""
```

---

## Tool Output Constraints

Keep tool outputs concise to avoid context bloat:

```python
# ❌ Bad: Returns 10k of raw data
@function_tool
def get_file(path: str) -> str:
    with open(path) as f:
        return f.read()  # Could be massive

# ✅ Good: Summarize or limit
@function_tool
def get_file_summary(path: str, lines: int = 50) -> str:
    """Get first N lines of file."""
    with open(path) as f:
        return "\n".join(f.readlines()[:lines])
```

---

## Multi-Tool Workflows

Agents chain tools automatically:

```python
@function_tool
def search(query: str) -> str:
    """Search database."""
    return "found: 3 results"

@function_tool
def analyze(data: str) -> str:
    """Analyze data."""
    return "analysis complete"

agent = Agent(
    name="Analyst",
    instructions="Search, then analyze results.",
    tools=[search, analyze],
    model="gpt-4o-mini",
)
# Agent will: search() → see results → analyze() → return final answer
```

---

## Common Patterns

### Pattern 1: API Integration

```python
@function_tool
async def get_user_orders(user_id: int) -> str:
    """Get all orders for a user from the orders API."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"/api/users/{user_id}/orders") as resp:
            orders = await resp.json()
            return json.dumps(orders, indent=2)
```

### Pattern 2: Database Query

```python
from sqlmodel import select, Session
from sqlalchemy import create_engine

@function_tool
def find_user_by_email(email: str) -> str:
    """Find a user by email address."""
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).first()
        if user:
            return f"User: {user.name} ({user.email})"
        return "User not found"
```

### Pattern 3: Calculation

```python
from decimal import Decimal

@function_tool
def calculate_tax(amount: Decimal, tax_rate: float = 0.1) -> str:
    """Calculate tax amount on a price."""
    tax = amount * Decimal(str(tax_rate))
    total = amount + tax
    return f"Amount: ${amount}, Tax: ${tax}, Total: ${total}"
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| No docstring | LLM doesn't know what tool does | Always add clear docstring |
| Generic names like `do_thing()` | LLM can't understand purpose | Use descriptive names |
| Huge output (10k+ chars) | Context overflow | Limit/summarize output |
| Unhelpful error messages | Agent confused on failure | Return clear error text |
| Side effects in docstring | Tool called unnecessarily | Keep docstring neutral |
| Hardcoded credentials | Security risk | Use environment variables |

---

## Best Practices

1. **Name tools by action**: `search_`, `get_`, `create_`, `delete_`
2. **Docstring = what LLM sees**: Make it clear and complete
3. **Type hints required**: `str`, `int`, `list[str]`, or Pydantic
4. **Return concise data**: 1-2 paragraphs, not raw dumps
5. **Handle errors gracefully**: Return error message, don't raise exception
6. **Use async for I/O**: Non-blocking for speed
7. **Test tool outputs**: Ensure LLM can understand and use results
