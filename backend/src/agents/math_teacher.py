"""Math Teacher Agent - Explains basic arithmetic concepts"""
from openai import AsyncOpenAI
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel
from agents.run import RunConfig
from src.config import settings
from pydantic import BaseModel
from typing import Optional


class MathExplanation(BaseModel):
    """Structured output from the math teacher"""
    concept: str
    explanation: str
    example: str
    tip: str


def get_llm_client() -> tuple[AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig]:
    """
    Create LLM client and model based on provider configuration.
    Returns: (client, model, run_config)
    """
    if settings.llm_provider == "openrouter":
        if not settings.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY not set in environment")

        client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.openrouter_api_key,
        )
        model = OpenAIChatCompletionsModel(
            model=settings.llm_model or "openai/gpt-4o-mini",
            openai_client=client,
        )
        run_config = RunConfig(
            model=model,
            model_provider=client,
            tracing_disabled=True,  # Required for non-OpenAI providers
        )

    elif settings.llm_provider == "gemini":
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not set in environment")

        client = AsyncOpenAI(
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=settings.gemini_api_key,
        )
        model = OpenAIChatCompletionsModel(
            model="gemini-2.5-flash",
            openai_client=client,
        )
        run_config = RunConfig(
            model=model,
            model_provider=client,
            tracing_disabled=True,
        )

    elif settings.llm_provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY not set in environment")

        client = AsyncOpenAI(api_key=settings.openai_api_key)
        model = OpenAIChatCompletionsModel(
            model="gpt-4o-mini",
            openai_client=client,
        )
        run_config = RunConfig(
            model=model,
            model_provider=client,
        )

    else:
        raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")

    return client, model, run_config


@function_tool
async def evaluate_math_expression(expression: str) -> str:
    """
    Safely evaluate a math expression (addition, subtraction, multiplication, division).

    Args:
        expression: A math expression like "5 + 3" or "12 / 2"

    Returns:
        The result of the expression
    """
    # Simple safe evaluation - only allow basic arithmetic
    try:
        # Only allow numbers and basic operators
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return f"Invalid expression. Only basic arithmetic allowed."

        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"


@function_tool
async def get_arithmetic_tip(operation: str) -> str:
    """
    Get a helpful tip for a specific arithmetic operation.

    Args:
        operation: The operation ("addition", "subtraction", "multiplication", "division")

    Returns:
        A helpful tip for that operation
    """
    tips = {
        "addition": "When adding numbers, line them up by place value (ones, tens, hundreds, etc.). Add from right to left, carrying over when you get 10 or more.",
        "subtraction": "When subtracting, also line up by place value. Subtract from right to left. If you can't subtract the bottom number from the top, borrow from the next place value.",
        "multiplication": "Break numbers into parts (e.g., 23 = 20 + 3), multiply each part separately, then add them together. This is the distributive property!",
        "division": "Division is the opposite of multiplication. Think of it as breaking a number into equal groups. Use long division for larger numbers.",
    }

    operation = operation.lower()
    return tips.get(operation, f"No specific tip available for '{operation}'")


async def create_math_teacher_agent() -> Agent:
    """
    Create the Math Teacher Agent that explains arithmetic concepts.

    Returns:
        An Agent configured to teach basic arithmetic
    """
    _, model, _ = get_llm_client()

    agent = Agent(
        name="Math Teacher",
        instructions="""You are a friendly and patient math teacher who specializes in explaining basic arithmetic concepts.

Your role is to:
1. Explain arithmetic concepts (addition, subtraction, multiplication, division) in simple, clear language
2. Provide real-world examples that make concepts easy to understand
3. Use the available tools to evaluate expressions and provide tips
4. Encourage learning and build confidence in math skills

When explaining math:
- Start with the concept definition
- Give a step-by-step explanation
- Provide a concrete example
- Share a helpful tip or trick
- Ask if they want to understand anything better

Keep explanations appropriate for beginners. Avoid jargon when possible.""",
        model=model,
        tools=[evaluate_math_expression, get_arithmetic_tip],
        output_type=MathExplanation,
    )

    return agent


async def explain_math(user_question: str) -> MathExplanation:
    """
    Ask the math teacher to explain a concept.

    Args:
        user_question: The user's question about math

    Returns:
        MathExplanation with structured output
    """
    agent = await create_math_teacher_agent()
    _, _, run_config = get_llm_client()

    result = await Runner.run(
        agent,
        user_question,
        run_config=run_config,
        max_turns=10,
    )

    return result.final_output
