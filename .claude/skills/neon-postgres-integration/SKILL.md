---
name: neon-postgres-integration
description: |
  This skill should be used when configuring Neon database connections, creating migrations, or writing database queries.
  Use for connection setup and database operations with Neon Serverless PostgreSQL.
---

# Neon Postgres Integration Skill

Auto-invoke when configuring Neon database connections, creating migrations, or writing database queries. Use for connection setup and database operations.

## Neon Connection String Format

Neon uses a specific connection string format that includes connection pooling information:

### Basic Format
```
postgresql://[user]:[password]@[host]:[port]/[database]?sslmode=require
```

### Neon-Specific Format
```
postgresql://[username]:[password]@[neon-project-name].[region].neon.tech:5432/[database-name]?sslmode=require
```

### Example Connection Strings
```bash
# Production connection
postgresql://myuser:mypassword@myproject.us-east-1.aws.neon.tech:5432/mydatabase?sslmode=require

# With connection pool settings
postgresql://myuser:mypassword@myproject.us-east-1.aws.neon.tech:5432/mydatabase?sslmode=require&pool_timeout=30&command_timeout=60

# For local development with Neon
postgresql://localuser:localpass@localhost:5432/localdb
```

## SQLModel Engine Configuration

Configure SQLModel with proper Neon settings for optimal performance:

### Basic Engine Setup
```python
from sqlmodel import create_engine
from sqlalchemy.pool import QueuePool
import os

# Basic engine configuration
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for debugging SQL queries
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,  # Recycle connections every 5 minutes
    pool_size=5,       # Initial pool size
    max_overflow=10,   # Maximum additional connections
    poolclass=QueuePool
)
```

### Production-Ready Engine Configuration
```python
from sqlmodel import create_engine
from sqlalchemy.pool import QueuePool
import os
from urllib.parse import urlparse

def create_neon_engine():
    """Create SQLModel engine optimized for Neon Serverless"""
    database_url = os.getenv("DATABASE_URL")

    # Parse URL to extract components
    parsed = urlparse(database_url)

    # Configure engine with Neon-specific settings
    engine = create_engine(
        database_url,
        echo=os.getenv("DEBUG", "False").lower() == "true",
        pool_pre_ping=True,           # Verify connections before use
        pool_recycle=300,             # Recycle connections every 5 minutes
        pool_size=5,                  # Initial pool size (Neon recommends 5-10)
        max_overflow=10,              # Max additional connections
        pool_timeout=30,              # Timeout for getting connection from pool
        poolclass=QueuePool,
        connect_args={
            "connect_timeout": 10,     # Connection timeout
            "application_name": "myapp" # Application name for monitoring
        }
    )

    return engine

engine = create_neon_engine()
```

## Connection Pooling with Neon

Neon Serverless has specific requirements for connection pooling due to its serverless nature:

### Recommended Pool Settings
```python
from sqlalchemy.pool import QueuePool

NEON_POOL_SETTINGS = {
    "pool_size": 5,           # Smaller pool size recommended for Neon
    "max_overflow": 10,       # Limit overflow connections
    "pool_timeout": 30,       # Timeout when pool is exhausted
    "pool_recycle": 300,      # Recycle connections to avoid stale connections
    "pool_pre_ping": True,    # Verify connections before use
    "echo": False             # Enable for debugging
}

def get_neon_engine():
    return create_engine(
        os.getenv("DATABASE_URL"),
        **NEON_POOL_SETTINGS
    )
```

### Connection Pool Monitoring
```python
def monitor_connection_pool(engine):
    """Monitor connection pool status"""
    pool = engine.pool
    stats = {
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
        "size": pool.size()
    }
    return stats

# Example usage
stats = monitor_connection_pool(engine)
print(f"Pool stats: {stats}")
```

## Environment Variable Setup (DATABASE_URL)

Proper environment configuration for Neon integration:

### Environment Variables (.env)
```bash
# Database configuration
DATABASE_URL=postgresql://username:password@myproject.region.neon.tech:5432/dbname?sslmode=require

# Optional settings
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
DATABASE_POOL_TIMEOUT=30
DATABASE_RECYCLE_TIME=300
```

### Configuration Class
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_RECYCLE_TIME: int = 300

    # Other settings
    DEBUG: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
```

## SSL Requirements for Neon

Neon requires SSL connections and has specific SSL configuration requirements:

### SSL Configuration
```python
import ssl
from sqlalchemy import create_engine

def create_ssl_engine():
    """Create engine with proper SSL configuration for Neon"""
    database_url = os.getenv("DATABASE_URL")

    # Ensure SSL is required for Neon
    if "sslmode=require" not in database_url:
        # Add SSL requirement to URL
        separator = "&" if "?" in database_url else "?"
        database_url = f"{database_url}{separator}sslmode=require"

    engine = create_engine(
        database_url,
        connect_args={
            "sslmode": "require",
            "sslcert": os.getenv("SSL_CERT_PATH"),  # Optional
            "sslkey": os.getenv("SSL_KEY_PATH"),    # Optional
            "sslrootcert": os.getenv("SSL_ROOT_CERT_PATH")  # Optional
        }
    )

    return engine
```

### SSL Certificate Validation
```python
def validate_ssl_connection(engine):
    """Validate SSL connection to Neon"""
    try:
        with engine.connect() as conn:
            # Test SSL connection
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]

            # Check if connection is using SSL
            ssl_check = conn.execute(text("SELECT ssl_is_used();"))
            is_ssl = ssl_check.fetchone()[0]

            if not is_ssl:
                raise Exception("SSL is not enabled for this connection")

            return {"version": version, "ssl_enabled": is_ssl}
    except Exception as e:
        raise Exception(f"SSL connection validation failed: {str(e)}")
```

## Migration Strategy with Alembic

Proper migration setup for Neon Serverless PostgreSQL:

### Alembic Configuration (alembic.ini)
```ini
[alembic]
# Path to migration scripts
script_location = alembic

# Template used to generate migration files
# file_template = %%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python-dateutil library that can be
# installed by adding `alembic[tz]` to the pip requirements
# string value is passed to dateutil.tz.gettz()
# leave blank for localtime
# timezone =

# max length of characters to apply to the
# "slug" field
# max_length = 40

# version_num length, if version_table is used
# version_num_length = 32

# version_locations, if specified, will override the value of "script_location"
# version_locations = %(here)s/bar:%(here)s/bat

# The logging configuration file to use.
# This file is used when alembic is called with the
# `-l` option to specify a logging configuration file.
logging_config_file = alembic/log.conf

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

### Alembic Environment Configuration (alembic/env.py)
```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from sqlmodel import SQLModel
import os

# Import your models here to register them
from app.models.user import User  # Example import
from app.models.todo import Todo  # Example import

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata
target_metadata = SQLModel.metadata

def get_url():
    """Get database URL from environment"""
    return os.getenv("DATABASE_URL")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # Compare column types
        compare_server_default=True  # Compare server defaults
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Migration Commands
```bash
# Generate a new migration
alembic revision --autogenerate -m "Add users table"

# Apply migrations
alembic upgrade head

# Check current migration status
alembic current

# Downgrade to previous version
alembic downgrade -1

# Show migration history
alembic history --verbose
```

## Connection Health Checks

Implement health checks for Neon database connections:

### Basic Health Check
```python
from sqlalchemy import text
from typing import Dict, Any

def check_database_health(engine) -> Dict[str, Any]:
    """Check database connection health"""
    try:
        with engine.connect() as conn:
            # Test basic connectivity
            result = conn.execute(text("SELECT 1"))
            connected = result.fetchone() is not None

            # Check database version
            version_result = conn.execute(text("SELECT version()"))
            version = version_result.fetchone()[0]

            # Check SSL status
            ssl_result = conn.execute(text("SELECT ssl_is_used()"))
            ssl_enabled = ssl_result.fetchone()[0]

            return {
                "status": "healthy",
                "connected": connected,
                "version": version,
                "ssl_enabled": ssl_enabled,
                "timestamp": datetime.utcnow().isoformat()
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

# Example usage in a health check endpoint
@app.get("/health/db")
async def database_health_check():
    health = check_database_health(engine)
    status_code = 200 if health["status"] == "healthy" else 503
    return JSONResponse(content=health, status_code=status_code)
```

### Advanced Health Check
```python
def advanced_health_check(engine) -> Dict[str, Any]:
    """Advanced database health check with performance metrics"""
    import time

    start_time = time.time()

    try:
        with engine.connect() as conn:
            # Test query timing
            query_start = time.time()
            result = conn.execute(text("SELECT 1"))
            query_time = time.time() - query_start

            # Test connection pool status
            pool = engine.pool
            pool_stats = {
                "checked_out": pool.checkedout(),
                "overflow": pool.overflow(),
                "size": pool.size()
            }

            # Test write/read cycle
            test_start = time.time()
            conn.execute(text("CREATE TEMP TABLE test_health_check (id INTEGER);"))
            conn.execute(text("INSERT INTO test_health_check VALUES (1);"))
            test_result = conn.execute(text("SELECT * FROM test_health_check;"))
            test_data = test_result.fetchall()
            test_time = time.time() - test_start

            total_time = time.time() - start_time

            return {
                "status": "healthy",
                "connection_time": query_time,
                "test_operation_time": test_time,
                "total_response_time": total_time,
                "pool_stats": pool_stats,
                "can_write_read": len(test_data) > 0,
                "timestamp": datetime.utcnow().isoformat()
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "total_response_time": time.time() - start_time,
            "timestamp": datetime.utcnow().isoformat()
        }
```

## Error Handling for Database Operations

Comprehensive error handling for Neon database operations:

### Database Error Handler
```python
from sqlalchemy.exc import (
    DatabaseError,
    IntegrityError,
    OperationalError,
    ProgrammingError
)
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

def handle_database_errors(exc: Exception) -> HTTPException:
    """Convert database exceptions to appropriate HTTP responses"""

    if isinstance(exc, IntegrityError):
        # Handle constraint violations
        logger.error(f"Integrity error: {exc}")
        return HTTPException(
            status_code=409,
            detail="Data integrity violation. Check for duplicate entries or invalid references."
        )

    elif isinstance(exc, OperationalError):
        # Handle operational errors (connection issues, timeouts)
        logger.error(f"Operational error: {exc}")
        return HTTPException(
            status_code=503,
            detail="Database temporarily unavailable. Please try again later."
        )

    elif isinstance(exc, ProgrammingError):
        # Handle programming errors (invalid SQL, schema issues)
        logger.error(f"Programming error: {exc}")
        return HTTPException(
            status_code=500,
            detail="Database configuration error. Please contact support."
        )

    elif isinstance(exc, DatabaseError):
        # Handle general database errors
        logger.error(f"Database error: {exc}")
        return HTTPException(
            status_code=500,
            detail="Database operation failed. Please try again later."
        )

    else:
        # Handle unexpected database errors
        logger.error(f"Unexpected database error: {exc}")
        return HTTPException(
            status_code=500,
            detail="An unexpected database error occurred."
        )
```

### Safe Database Operations
```python
from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError

@contextmanager
def safe_db_operation(session):
    """Context manager for safe database operations with error handling"""
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise handle_database_errors(e)
    except Exception as e:
        session.rollback()
        logger.error(f"Unexpected error in database operation: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during database operation."
        )

# Example usage in endpoint
@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, session: Session = Depends(get_session)):
    try:
        db_user = User.model_validate(user.model_dump())

        with safe_db_operation(session):
            session.add(db_user)
            session.flush()  # Get ID without committing
            user_id = db_user.id

        # Refresh to get full object after commit
        session.refresh(db_user)
        return db_user
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Failed to create user")
```

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing database configuration, SQLModel models, Alembic setup, environment variables |
| **Conversation** | User's specific requirements for Neon integration, migration needs, connection settings |
| **Skill References** | Neon and PostgreSQL patterns from `references/` (connections, migrations, error handling) |
| **User Guidelines** | Project-specific conventions, team standards, security requirements |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).