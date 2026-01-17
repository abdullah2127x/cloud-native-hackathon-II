"""Database connection and session management"""
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator


# Database URL will be configured via environment
DATABASE_URL = "sqlite:///./test.db"  # Placeholder - will be overridden by config

# Create engine
engine = create_engine(
    DATABASE_URL,
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
