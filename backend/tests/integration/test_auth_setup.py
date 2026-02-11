"""
Integration tests for Better Auth setup and migration

Reference: specs/001-todo-web-crud/spec.md
Task: T039 - Generate integration test for Better Auth migration

These tests verify that:
1. The user table exists with correct schema
2. User table has correct columns and constraints
3. Database operations work correctly

Uses isolated in-memory SQLite engine to avoid polluting
the production database and to be dialect-agnostic.
"""
import pytest
from datetime import datetime, UTC
from sqlalchemy import inspect as sa_inspect, text
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, select, create_engine

from src.models.user import User  # noqa: F401 — registers model with SQLModel metadata


@pytest.fixture(name="auth_engine", scope="class")
def auth_engine_fixture():
    """Isolated in-memory SQLite engine for auth schema tests"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="auth_session")
def auth_session_fixture(auth_engine):
    """Session with rollback after each test for isolation"""
    with Session(auth_engine) as session:
        yield session
        session.rollback()


class TestBetterAuthMigration:
    """Test suite for Better Auth database migration"""

    def test_user_table_exists(self, auth_engine):
        """Test that the user table was created"""
        inspector = sa_inspect(auth_engine)
        table_names = inspector.get_table_names()
        assert "user" in table_names, "User table should exist"

    def test_user_table_has_required_columns(self, auth_engine):
        """Test that user table has all required columns"""
        required_columns = {"id", "email", "name", "emailVerified", "createdAt", "updatedAt"}
        inspector = sa_inspect(auth_engine)
        columns = {col["name"] for col in inspector.get_columns("user")}
        assert required_columns.issubset(columns), \
            f"Missing columns: {required_columns - columns}"

    def test_user_table_email_has_unique_constraint(self, auth_engine):
        """Test that email column has a unique constraint or index"""
        inspector = sa_inspect(auth_engine)
        unique_constraints = inspector.get_unique_constraints("user")
        indexes = inspector.get_indexes("user")
        email_unique = (
            any("email" in uc.get("column_names", []) for uc in unique_constraints)
            or any(
                idx.get("unique") and "email" in idx.get("column_names", [])
                for idx in indexes
            )
        )
        assert email_unique, "Email column should have a unique constraint or index"

    def test_user_id_is_primary_key(self, auth_engine):
        """Test that id column is the primary key"""
        inspector = sa_inspect(auth_engine)
        pk = inspector.get_pk_constraint("user")
        assert "id" in pk.get("constrained_columns", []), \
            "id column should be the primary key"

    def test_database_connection_is_working(self, auth_session):
        """Test that database connection is working"""
        result = auth_session.exec(text("SELECT 1"))
        value = result.first()
        assert value is not None
        assert value[0] == 1

    def test_can_insert_user_record(self, auth_session):
        """Test that user records can be inserted"""
        user = User(
            id="insert-test-user",
            email="insert@example.com",
            name="Insert Test",
            emailVerified=False,
            createdAt=datetime.now(UTC),
            updatedAt=datetime.now(UTC),
        )
        auth_session.add(user)
        auth_session.commit()
        auth_session.refresh(user)

        retrieved = auth_session.get(User, "insert-test-user")
        assert retrieved is not None
        assert retrieved.email == "insert@example.com"
        assert retrieved.name == "Insert Test"

    def test_duplicate_email_is_prevented(self, auth_session):
        """Test that duplicate emails are prevented by unique constraint"""
        user1 = User(
            id="dup-user-1",
            email="dup@example.com",
            name="User One",
            createdAt=datetime.now(UTC),
            updatedAt=datetime.now(UTC),
        )
        user2 = User(
            id="dup-user-2",
            email="dup@example.com",  # Same email
            name="User Two",
            createdAt=datetime.now(UTC),
            updatedAt=datetime.now(UTC),
        )
        auth_session.add(user1)
        auth_session.commit()

        with pytest.raises(Exception):
            auth_session.add(user2)
            auth_session.commit()

    def test_can_query_users_by_email(self, auth_session):
        """Test that users can be queried by email"""
        user = User(
            id="query-test-user",
            email="query@example.com",
            name="Query Test",
            createdAt=datetime.now(UTC),
            updatedAt=datetime.now(UTC),
        )
        auth_session.add(user)
        auth_session.commit()

        statement = select(User).where(User.email == "query@example.com")
        retrieved = auth_session.exec(statement).first()
        assert retrieved is not None
        assert retrieved.id == "query-test-user"
        assert retrieved.email == "query@example.com"
