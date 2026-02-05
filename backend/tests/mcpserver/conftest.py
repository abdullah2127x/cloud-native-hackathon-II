"""Pytest fixtures for MCP server tests"""

import json
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
from jwt import encode
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

from src.config import settings
from src.models.task import Task

# Use SQLite in-memory for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(name="database_session")
async def database_session_fixture() -> AsyncGenerator[AsyncSession, None]:
    """Create in-memory SQLite database session for tests

    Yields:
        AsyncSession for database operations
    """
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest.fixture(name="mock_jwt_token")
def mock_jwt_token_fixture() -> str:
    """Create a mock JWT token for testing

    Returns:
        Valid JWT token with test user_id
    """
    payload = {
        "sub": "test-user-123",  # User ID
        "iat": 1234567890,
        "exp": 9999999999,  # Far in future
    }

    token = encode(
        payload,
        settings.better_auth_secret,
        algorithm="HS256",
    )

    return token


@pytest.fixture(name="mock_auth_header")
def mock_auth_header_fixture(mock_jwt_token: str) -> str:
    """Create a mock Authorization header

    Args:
        mock_jwt_token: JWT token fixture

    Returns:
        Authorization header value
    """
    return f"Bearer {mock_jwt_token}"


@pytest.fixture(name="mock_user_id")
def mock_user_id_fixture() -> str:
    """Get test user ID

    Returns:
        Test user ID
    """
    return "test-user-123"


@pytest.fixture(name="sample_task")
async def sample_task_fixture(
    database_session: AsyncSession, mock_user_id: str
) -> Task:
    """Create a sample task in database

    Args:
        database_session: Database session
        mock_user_id: Test user ID

    Returns:
        Created Task object
    """
    task = Task(
        user_id=mock_user_id,
        title="Sample Task",
        description="This is a sample task",
        completed=False,
    )

    database_session.add(task)
    await database_session.commit()
    await database_session.refresh(task)

    return task


@pytest.fixture(name="sample_tasks")
async def sample_tasks_fixture(
    database_session: AsyncSession, mock_user_id: str
) -> list[Task]:
    """Create multiple sample tasks

    Args:
        database_session: Database session
        mock_user_id: Test user ID

    Returns:
        List of created Task objects
    """
    tasks = [
        Task(
            user_id=mock_user_id,
            title="Task 1",
            description="First task",
            completed=False,
        ),
        Task(
            user_id=mock_user_id,
            title="Task 2",
            description="Second task",
            completed=True,
        ),
        Task(
            user_id=mock_user_id,
            title="Task 3",
            description="Third task",
            completed=False,
        ),
    ]

    for task in tasks:
        database_session.add(task)

    await database_session.commit()

    for task in tasks:
        await database_session.refresh(task)

    return tasks


@pytest.fixture(name="mock_mcp_context")
def mock_mcp_context_fixture() -> dict:
    """Create a mock MCP request context

    Returns:
        Mock context dictionary
    """
    return {
        "user_id": "test-user-123",
        "request_id": "req-123",
        "timestamp": "2026-02-05T12:00:00Z",
    }
