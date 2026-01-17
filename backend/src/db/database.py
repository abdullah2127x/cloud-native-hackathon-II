"""Database connection and session management"""
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator

# Import all models so SQLModel knows about them when creating tables
from src.models.user import User  # noqa: F401
from src.models.task import Task  # noqa: F401
from src.config import settings


# Create engine
engine = create_engine(
    settings.database_url,
    echo=False,  # Set to True for SQL debugging
    connect_args={"check_same_thread": False},  # Needed for SQLite
)


def create_db_and_tables():
    """Create all database tables"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session
