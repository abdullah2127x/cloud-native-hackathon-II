# Neon Postgres Integration - Best Practices and Common Patterns

## Connection Configuration Best Practices

### ✅ DO: Use Appropriate Pool Sizes for Neon
Neon Serverless has specific recommendations for connection pool sizes:

```python
# Good: Neon-optimized pool configuration
from sqlmodel import create_engine
from sqlalchemy.pool import QueuePool

def create_neon_engine():
    return create_engine(
        os.getenv("DATABASE_URL"),
        pool_size=5,        # Recommended: 5-10 for Neon
        max_overflow=10,    # Keep overflow reasonable
        pool_timeout=30,    # Reasonable timeout
        pool_recycle=300,   # Recycle connections to avoid stale connections
        pool_pre_ping=True, # Verify connections before use
        poolclass=QueuePool
    )
```

### ❌ AVOID: Large Pool Sizes
```python
# Avoid: Large pool sizes that waste Neon resources
def create_bad_engine():
    return create_engine(
        os.getenv("DATABASE_URL"),
        pool_size=50,       # Too large for Neon Serverless
        max_overflow=100,   # This could cause issues
        pool_timeout=10     # Too short
    )
```

## SSL and Security Best Practices

### ✅ DO: Always Require SSL for Neon
```python
# Good: Ensure SSL is always enabled
def ensure_ssl_connection(database_url: str):
    if "sslmode=require" not in database_url:
        separator = "&" if "?" in database_url else "?"
        database_url = f"{database_url}{separator}sslmode=require"
    return database_url

# Use in engine creation
def create_secure_engine():
    url = ensure_ssl_connection(os.getenv("DATABASE_URL"))
    return create_engine(url, connect_args={"sslmode": "require"})
```

### ✅ DO: Validate SSL Connection
```python
# Good: Verify SSL is properly configured
def validate_ssl_connection(engine):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT ssl_is_used();"))
        is_ssl = result.fetchone()[0]
        if not is_ssl:
            raise Exception("SSL is not enabled for this connection")
        return True
```

## Migration Best Practices

### ✅ DO: Use Alembic with Neon-Specific Settings
```python
# Good: Alembic configuration optimized for Neon
def run_migrations_online():
    """Run migrations with Neon-optimized settings"""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # Use NullPool for migrations
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Compare column types
            compare_server_default=True,  # Compare server defaults
            # Neon-specific settings
            include_object=include_object,  # Custom filter function if needed
        )

        with context.begin_transaction():
            context.run_migrations()
```

### ✅ DO: Test Migrations Before Applying
```python
# Good: Dry run migrations before applying
def test_migration_safety():
    """Test migration safety before applying"""
    # Generate migration script
    alembic_cfg = Config("alembic/alembic.ini")

    # Check for potential issues
    # This is a simplified example - in practice, you'd want more thorough checks
    try:
        # Try connecting to a test database
        test_url = os.getenv("TEST_DATABASE_URL")
        test_engine = create_engine(test_url)

        # Apply migration to test database first
        # This should be done in a separate test environment
        pass
    except Exception as e:
        raise Exception(f"Migration test failed: {e}")
```

## Error Handling Best Practices

### ✅ DO: Implement Comprehensive Error Handling
```python
# Good: Comprehensive error handling
from sqlalchemy.exc import (
    DatabaseError,
    IntegrityError,
    OperationalError,
    ProgrammingError
)

def handle_database_error(exc: Exception):
    """Handle database errors appropriately"""

    if isinstance(exc, IntegrityError):
        # Handle constraint violations gracefully
        if 'unique constraint' in str(exc):
            return {"error": "Unique constraint violation", "code": "UNIQUE_VIOLATION"}
        elif 'foreign key constraint' in str(exc):
            return {"error": "Foreign key constraint violation", "code": "FK_VIOLATION"}

    elif isinstance(exc, OperationalError):
        # Handle connection and operational errors
        if 'timeout' in str(exc).lower():
            return {"error": "Database timeout", "code": "TIMEOUT"}
        elif 'connection' in str(exc).lower():
            return {"error": "Connection error", "code": "CONNECTION_ERROR"}

    elif isinstance(exc, ProgrammingError):
        # Handle SQL syntax or schema errors
        return {"error": "Programming error", "code": "PROGRAMMING_ERROR"}

    else:
        # Handle other database errors
        return {"error": "Database error", "code": "DATABASE_ERROR"}
```

### ✅ DO: Use Context Managers for Safe Operations
```python
# Good: Context manager for safe database operations
from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError

@contextmanager
def safe_db_transaction(session):
    """Context manager for safe database transactions"""
    try:
        yield session
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Usage
def create_user_safe(user_data):
    with Session(engine) as session:
        with safe_db_transaction(session):
            user = User(**user_data)
            session.add(user)
            session.flush()  # Get ID without committing
            return user.id
```

## Health Check Best Practices

### ✅ DO: Implement Multi-Level Health Checks
```python
# Good: Comprehensive health check implementation
import time
from typing import Dict, Any

def comprehensive_health_check(engine) -> Dict[str, Any]:
    """Perform comprehensive health check with multiple levels"""

    # Level 1: Basic connectivity
    start_time = time.time()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            basic_connectivity = result.fetchone() is not None
    except Exception as e:
        return {
            "status": "critical",
            "message": f"Cannot connect to database: {str(e)}",
            "response_time": time.time() - start_time
        }

    # Level 2: Performance check
    try:
        query_start = time.time()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM information_schema.tables"))
            table_count = result.fetchone()[0]
        performance_time = time.time() - query_start
    except Exception as e:
        return {
            "status": "degraded",
            "message": f"Performance check failed: {str(e)}",
            "basic_connectivity": True,
            "response_time": time.time() - start_time
        }

    # Level 3: Feature check
    try:
        with engine.connect() as conn:
            # Test write/read operations
            conn.execute(text("CREATE TEMP TABLE health_test (id INTEGER);"))
            conn.execute(text("INSERT INTO health_test VALUES (1);"))
            result = conn.execute(text("SELECT * FROM health_test;"))
            can_write_read = len(result.fetchall()) > 0
            conn.execute(text("DROP TABLE health_test;"))
    except Exception as e:
        return {
            "status": "degraded",
            "message": f"Write/read test failed: {str(e)}",
            "basic_connectivity": True,
            "response_time": time.time() - start_time
        }

    # All checks passed
    total_time = time.time() - start_time
    return {
        "status": "healthy",
        "basic_connectivity": True,
        "can_write_read": can_write_read,
        "performance_time": performance_time,
        "response_time": total_time,
        "table_count": table_count
    }
```

## Environment and Configuration Best Practices

### ✅ DO: Use Environment-Specific Configuration
```python
# Good: Environment-specific configuration
import os
from pydantic_settings import BaseSettings

class DatabaseSettings(BaseSettings):
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_RECYCLE_TIME: int = 300
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

def get_db_settings():
    """Get database settings based on environment"""
    settings = DatabaseSettings()

    # Adjust settings based on environment
    env = os.getenv("ENVIRONMENT", "development")

    if env == "production":
        settings.DATABASE_POOL_SIZE = 10
        settings.DATABASE_MAX_OVERFLOW = 20
        settings.DATABASE_POOL_TIMEOUT = 60
    elif env == "development":
        settings.DATABASE_POOL_SIZE = 2
        settings.DATABASE_MAX_OVERFLOW = 5
        settings.DEBUG = True

    return settings
```

### ✅ DO: Validate Configuration at Startup
```python
# Good: Configuration validation
def validate_database_config():
    """Validate database configuration at application startup"""
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL environment variable is required")

    if "sslmode=require" not in database_url:
        raise ValueError("DATABASE_URL must include sslmode=require for Neon")

    if not database_url.startswith("postgresql://"):
        raise ValueError("DATABASE_URL must use PostgreSQL protocol")

    # Validate pool settings
    pool_size = int(os.getenv("DATABASE_POOL_SIZE", "5"))
    if pool_size < 1 or pool_size > 50:
        raise ValueError("DATABASE_POOL_SIZE should be between 1 and 50")

    print("Database configuration validated successfully")
```

## Common Anti-Patterns to Avoid

### ❌ Anti-pattern: Hardcoded Connection Strings
```python
# Avoid: Hardcoded connection strings
def create_bad_engine():
    # Never hardcode credentials
    return create_engine("postgresql://user:password@host:port/dbname")
```

### ✅ Solution: Use Environment Variables
```python
# Good: Use environment variables
def create_good_engine():
    return create_engine(os.getenv("DATABASE_URL"))
```

### ❌ Anti-pattern: No Connection Timeout Handling
```python
# Avoid: No timeout configuration
def create_unsafe_engine():
    return create_engine(
        os.getenv("DATABASE_URL"),
        pool_timeout=0  # This means wait indefinitely!
    )
```

### ✅ Solution: Set Reasonable Timeouts
```python
# Good: Set reasonable timeouts
def create_safe_engine():
    return create_engine(
        os.getenv("DATABASE_URL"),
        pool_timeout=30,      # 30 seconds timeout
        connect_args={
            "connect_timeout": 10  # 10 seconds connection timeout
        }
    )
```

### ❌ Anti-pattern: Not Handling Migration Conflicts
```python
# Avoid: Not handling migration conflicts
def run_migrations_unsafe():
    # This could cause issues if migrations conflict
    subprocess.run(["alembic", "upgrade", "head"])
```

### ✅ Solution: Safe Migration Handling
```python
# Good: Safe migration handling
def run_migrations_safe():
    try:
        # Check current state before migrating
        result = subprocess.run(["alembic", "current"], capture_output=True, text=True)
        current = result.stdout.strip()

        # Run migration
        result = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"Migration failed: {result.stderr}")

        print(f"Migrations completed successfully. Current: {current}")
    except Exception as e:
        print(f"Migration error: {e}")
        raise
```

## Performance Optimization Patterns

### ✅ DO: Implement Connection Pool Monitoring
```python
# Good: Monitor connection pool usage
import logging

logger = logging.getLogger(__name__)

def monitor_pool_usage(engine):
    """Monitor and log connection pool usage"""
    pool = engine.pool
    stats = {
        "checked_out": pool.checkedout(),
        "size": pool.size(),
        "utilization": pool.checkedout() / pool.size() if pool.size() > 0 else 0
    }

    # Log warning if utilization is high
    if stats["utilization"] > 0.8:
        logger.warning(f"High connection pool utilization: {stats['utilization']:.2%}")

    return stats
```

### ✅ DO: Use Connection Pre-warming
```python
# Good: Pre-warm connections to reduce latency
def prewarm_connections(engine, num_connections: int = 3):
    """Pre-warm database connections to reduce initial latency"""
    connections = []

    try:
        for i in range(num_connections):
            conn = engine.connect()
            # Execute a simple query to establish the connection
            conn.execute(text("SELECT 1"))
            connections.append(conn)

        # Close connections (they'll return to the pool)
        for conn in connections:
            conn.close()

        logger.info(f"Pre-warmed {num_connections} database connections")
    except Exception as e:
        logger.error(f"Failed to prewarm connections: {e}")
```

## Testing Best Practices

### ✅ DO: Use Test Databases
```python
# Good: Use separate test database configuration
import pytest
from sqlmodel import create_engine
from sqlalchemy.pool import StaticPool

@pytest.fixture(scope="function")
def test_engine():
    """Create test database engine with memory pool"""
    test_url = os.getenv("TEST_DATABASE_URL")
    if not test_url:
        # Use in-memory SQLite for testing if no test DB provided
        test_url = "sqlite:///./test.db"

    engine = create_engine(
        test_url,
        # Use StaticPool for testing to avoid connection issues
        poolclass=StaticPool if "sqlite" in test_url else None,
        # Echo SQL for debugging tests
        echo=os.getenv("TEST_DEBUG", "False").lower() == "true"
    )

    yield engine

    # Cleanup if needed
    engine.dispose()
```

## Monitoring and Observability

### ✅ DO: Implement Database Metrics
```python
# Good: Track database metrics
from typing import Dict, Any
import time

class DatabaseMetrics:
    """Track database performance metrics"""

    def __init__(self):
        self.query_count = 0
        self.total_query_time = 0
        self.error_count = 0

    def track_query(self, query_time: float, success: bool = True):
        """Track query execution metrics"""
        self.query_count += 1
        self.total_query_time += query_time

        if not success:
            self.error_count += 1

    def get_metrics(self) -> Dict[str, Any]:
        """Get current database metrics"""
        avg_query_time = (
            self.total_query_time / self.query_count if self.query_count > 0 else 0
        )

        return {
            "query_count": self.query_count,
            "total_query_time": self.total_query_time,
            "avg_query_time": avg_query_time,
            "error_count": self.error_count,
            "error_rate": (
                self.error_count / self.query_count if self.query_count > 0 else 0
            )
        }

# Global metrics instance
db_metrics = DatabaseMetrics()
```