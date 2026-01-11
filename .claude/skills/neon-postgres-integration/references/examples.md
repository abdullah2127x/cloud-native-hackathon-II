# Neon Postgres Integration - Additional Examples

## Complete Example: Database Configuration Setup

### Configuration File Structure
```python
# config/database.py
from sqlmodel import create_engine
from sqlalchemy.pool import QueuePool
import os
from urllib.parse import urlparse
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseConfig:
    """Database configuration class for Neon integration"""

    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        self.pool_size = int(os.getenv("DATABASE_POOL_SIZE", "5"))
        self.max_overflow = int(os.getenv("DATABASE_MAX_OVERFLOW", "10"))
        self.pool_timeout = int(os.getenv("DATABASE_POOL_TIMEOUT", "30"))
        self.pool_recycle = int(os.getenv("DATABASE_RECYCLE_TIME", "300"))

        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is required")

    def create_engine(self):
        """Create SQLModel engine with Neon-optimized settings"""
        # Ensure SSL is required for Neon
        if "sslmode=require" not in self.database_url:
            separator = "&" if "?" in self.database_url else "?"
            self.database_url = f"{self.database_url}{separator}sslmode=require"

        engine = create_engine(
            self.database_url,
            pool_pre_ping=True,
            pool_recycle=self.pool_recycle,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            pool_timeout=self.pool_timeout,
            poolclass=QueuePool,
            echo=os.getenv("DEBUG_DB", "False").lower() == "true",
            connect_args={
                "connect_timeout": 10,
                "application_name": os.getenv("APP_NAME", "myapp"),
                "keepalives_idle": 300,
                "keepalives_interval": 30,
                "keepalives_count": 3
            }
        )

        logger.info("Database engine created successfully")
        return engine

# Initialize database configuration
db_config = DatabaseConfig()
engine = db_config.create_engine()
```

### Session Dependency
```python
# database/session.py
from sqlmodel import Session
from contextlib import contextmanager
from typing import Generator
from config.database import engine

def get_session() -> Generator[Session, None, None]:
    """Dependency to provide database session"""
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()

@contextmanager
def get_db_session():
    """Context manager for database operations"""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
```

## Migration Examples

### Alembic Migration Script Example
```python
# alembic/versions/001_create_users_table.py
"""Create users table

Revision ID: 001
Revises:
Create Date: 2024-01-01 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes

# revision identifiers
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create users table
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('first_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    # Create indexes
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)


def downgrade() -> None:
    # Drop users table
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
```

### Migration Management Script
```python
# scripts/manage_migrations.py
import subprocess
import sys
import os
from alembic.config import Config
from alembic import command

def run_migrations():
    """Run database migrations"""
    # Set environment
    os.environ['PYTHONPATH'] = '.'

    # Create alembic config
    alembic_cfg = Config("alembic/alembic.ini")

    # Run migrations
    command.upgrade(alembic_cfg, "head")
    print("Migrations completed successfully")

def create_migration(message: str):
    """Create a new migration"""
    os.environ['PYTHONPATH'] = '.'

    alembic_cfg = Config("alembic/alembic.ini")
    command.revision(alembic_cfg, autogenerate=True, message=message)
    print(f"Migration created: {message}")

def check_pending_migrations():
    """Check if there are pending migrations"""
    os.environ['PYTHONPATH'] = '.'

    alembic_cfg = Config("alembic/alembic.ini")

    # Get current revision
    from alembic.runtime.migration import MigrationContext
    from alembic.script import ScriptDirectory
    from sqlalchemy import create_engine

    engine = create_engine(os.getenv("DATABASE_URL"))

    with engine.connect() as conn:
        context = MigrationContext.configure(conn)
        script = ScriptDirectory.from_config(alembic_cfg)

        current_rev = context.get_current_revision()
        heads = script.get_heads()

        return current_rev not in heads

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python manage_migrations.py [run|create|check]")
        sys.exit(1)

    action = sys.argv[1]

    if action == "run":
        run_migrations()
    elif action == "create":
        if len(sys.argv) < 3:
            print("Usage: python manage_migrations.py create 'migration message'")
            sys.exit(1)
        create_migration(sys.argv[2])
    elif action == "check":
        has_pending = check_pending_migrations()
        print("Pending" if has_pending else "Up to date")
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)
```

## Health Check Implementation

### Complete Health Check Endpoint
```python
# api/health.py
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import time
from sqlalchemy import text
from database.session import engine
from datetime import datetime

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "neon-postgres-integration"
    }

@router.get("/database")
async def database_health_check():
    """Detailed database health check"""
    start_time = time.time()

    try:
        with engine.connect() as conn:
            # Test basic connectivity
            result = conn.execute(text("SELECT 1 as test"))
            connected = result.fetchone() is not None

            # Check database version
            version_result = conn.execute(text("SELECT version()"))
            version = version_result.fetchone()[0]

            # Check SSL status
            ssl_result = conn.execute(text("SELECT current_setting('is_superuser')"))
            # Note: This is a simplified check; actual SSL check may vary

            # Check connection pool
            pool = engine.pool
            pool_stats = {
                "checked_out": pool.checkedout(),
                "size": pool.size()
            }

            total_time = time.time() - start_time

            return {
                "status": "healthy",
                "connected": connected,
                "version": version.split()[0],  # Just the version number
                "response_time_ms": round(total_time * 1000, 2),
                "pool_stats": pool_stats,
                "timestamp": datetime.utcnow().isoformat()
            }
    except Exception as e:
        total_time = time.time() - start_time
        return {
            "status": "unhealthy",
            "error": str(e),
            "response_time_ms": round(total_time * 1000, 2),
            "timestamp": datetime.utcnow().isoformat()
        }

@router.get("/database/advanced")
async def advanced_database_health():
    """Advanced database health check with performance metrics"""
    start_time = time.time()

    try:
        with engine.connect() as conn:
            # Measure query response time
            query_start = time.time()
            result = conn.execute(text("SELECT 1"))
            query_time = (time.time() - query_start) * 1000  # Convert to ms

            # Test write operation
            write_start = time.time()
            conn.execute(text("CREATE TEMP TABLE health_test (id INTEGER, data TEXT);"))
            conn.execute(text("INSERT INTO health_test VALUES (1, 'test');"))
            read_result = conn.execute(text("SELECT * FROM health_test;"))
            read_data = read_result.fetchall()
            write_read_time = (time.time() - write_start) * 1000  # Convert to ms

            # Clean up
            conn.execute(text("DROP TABLE IF EXISTS health_test;"))

            # Get pool statistics
            pool = engine.pool
            pool_stats = {
                "checked_out": pool.checkedout(),
                "overflow": pool.overflow(),
                "size": pool.size(),
                "timeout": getattr(pool, 'timeout', 'N/A')
            }

            total_time = (time.time() - start_time) * 1000  # Convert to ms

            return {
                "status": "healthy",
                "basic_query_time_ms": round(query_time, 2),
                "write_read_cycle_time_ms": round(write_read_time, 2),
                "total_response_time_ms": round(total_time, 2),
                "pool_stats": pool_stats,
                "can_perform_write_read": len(read_data) > 0,
                "timestamp": datetime.utcnow().isoformat()
            }
    except Exception as e:
        total_time = (time.time() - start_time) * 1000  # Convert to ms
        return {
            "status": "unhealthy",
            "error": str(e),
            "total_response_time_ms": round(total_time, 2),
            "timestamp": datetime.utcnow().isoformat()
        }
```

## Error Handling Examples

### Comprehensive Error Handler
```python
# utils/db_errors.py
from sqlalchemy.exc import (
    DatabaseError,
    IntegrityError,
    OperationalError,
    ProgrammingError,
    DataError
)
from fastapi import HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class DatabaseErrorHandler:
    """Comprehensive database error handler for Neon PostgreSQL"""

    @staticmethod
    def handle_error(exc: Exception) -> HTTPException:
        """Convert database exceptions to appropriate HTTP responses"""

        error_details = {
            "original_error": str(exc),
            "error_type": type(exc).__name__,
            "timestamp": datetime.utcnow().isoformat()
        }

        if isinstance(exc, IntegrityError):
            # Handle constraint violations
            error_msg = DatabaseErrorHandler._parse_integrity_error(exc)
            logger.warning(f"Integrity error: {error_msg}")
            return HTTPException(
                status_code=409,
                detail={
                    "type": "INTEGRITY_ERROR",
                    "message": error_msg,
                    "details": error_details
                }
            )

        elif isinstance(exc, OperationalError):
            # Handle operational errors (connection issues, timeouts)
            error_msg = DatabaseErrorHandler._parse_operational_error(exc)
            logger.error(f"Operational error: {error_msg}")
            return HTTPException(
                status_code=503,
                detail={
                    "type": "OPERATIONAL_ERROR",
                    "message": error_msg,
                    "details": error_details
                }
            )

        elif isinstance(exc, ProgrammingError):
            # Handle programming errors (invalid SQL, schema issues)
            logger.error(f"Programming error: {exc}")
            return HTTPException(
                status_code=422,
                detail={
                    "type": "PROGRAMMING_ERROR",
                    "message": "Invalid query or schema issue",
                    "details": error_details
                }
            )

        elif isinstance(exc, DataError):
            # Handle data errors (invalid input, value too long, etc.)
            logger.warning(f"Data error: {exc}")
            return HTTPException(
                status_code=422,
                detail={
                    "type": "DATA_ERROR",
                    "message": "Invalid data provided",
                    "details": error_details
                }
            )

        elif isinstance(exc, DatabaseError):
            # Handle general database errors
            logger.error(f"Database error: {exc}")
            return HTTPException(
                status_code=500,
                detail={
                    "type": "DATABASE_ERROR",
                    "message": "Database operation failed",
                    "details": error_details
                }
            )

        else:
            # Handle unexpected errors
            logger.error(f"Unexpected database error: {exc}")
            return HTTPException(
                status_code=500,
                detail={
                    "type": "UNKNOWN_ERROR",
                    "message": "An unexpected database error occurred",
                    "details": error_details
                }
            )

    @staticmethod
    def _parse_integrity_error(exc: IntegrityError) -> str:
        """Parse integrity error to provide user-friendly message"""
        error_str = str(exc.orig)

        if "duplicate key value violates unique constraint" in error_str:
            # Extract constraint name
            if "users_email_key" in error_str:
                return "A user with this email already exists"
            elif "users_username_key" in error_str:
                return "A user with this username already exists"
            else:
                return "Duplicate entry not allowed"

        elif "violates foreign key constraint" in error_str:
            return "Referenced record does not exist"

        elif "violates not-null constraint" in error_str:
            return "Required field cannot be empty"

        else:
            return "Data integrity violation"

    @staticmethod
    def _parse_operational_error(exc: OperationalError) -> str:
        """Parse operational error to provide user-friendly message"""
        error_str = str(exc.orig)

        if "connection timeout" in error_str.lower():
            return "Database connection timed out"
        elif "too many connections" in error_str.lower():
            return "Database server is busy, please try again later"
        elif "could not connect" in error_str.lower():
            return "Unable to connect to database server"
        else:
            return "Database temporarily unavailable"

# Context manager for safe operations
from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError

@contextmanager
def safe_db_operation(session, logger=None):
    """Context manager for safe database operations with comprehensive error handling"""
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        if logger:
            logger.exception("Database operation failed")
        raise DatabaseErrorHandler.handle_error(e)
    except HTTPException:
        # Re-raise HTTP exceptions
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        if logger:
            logger.exception("Unexpected error in database operation")
        raise DatabaseErrorHandler.handle_error(e)
```

## Connection Pool Monitoring

### Connection Pool Monitoring Utility
```python
# utils/connection_monitor.py
from sqlalchemy.pool import Pool
from typing import Dict, Any
import threading
import time
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ConnectionPoolMonitor:
    """Monitor and manage connection pool for Neon PostgreSQL"""

    def __init__(self, engine, check_interval: int = 60):
        self.engine = engine
        self.check_interval = check_interval
        self.monitoring = False
        self.monitor_thread = None

    def get_pool_stats(self) -> Dict[str, Any]:
        """Get current connection pool statistics"""
        pool = self.engine.pool

        stats = {
            "timestamp": datetime.utcnow().isoformat(),
            "checked_out": pool.checkedout(),
            "size": pool.size(),
            "timeout": getattr(pool, 'timeout', 'N/A'),
            "pool_class": type(pool).__name__
        }

        # Add Neon-specific metrics if available
        try:
            # This might vary depending on pool implementation
            if hasattr(pool, 'overflow'):
                stats["overflow"] = pool.overflow()
        except:
            stats["overflow"] = "N/A"

        return stats

    def start_monitoring(self):
        """Start background monitoring of connection pool"""
        if self.monitoring:
            return

        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("Connection pool monitoring started")

    def stop_monitoring(self):
        """Stop connection pool monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("Connection pool monitoring stopped")

    def _monitor_loop(self):
        """Internal monitoring loop"""
        while self.monitoring:
            try:
                stats = self.get_pool_stats()

                # Log warnings if pool is near capacity
                if stats["checked_out"] >= stats["size"] * 0.8:
                    logger.warning(f"Connection pool at {stats['checked_out']}/{stats['size']} capacity")

                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Error in connection pool monitoring: {e}")
                time.sleep(self.check_interval)

    def get_recommendations(self) -> Dict[str, str]:
        """Get recommendations based on current pool usage"""
        stats = self.get_pool_stats()

        recommendations = []

        if stats["checked_out"] >= stats["size"]:
            recommendations.append("Consider increasing pool_size or max_overflow")

        if stats["checked_out"] < stats["size"] * 0.2:
            recommendations.append("Pool size might be too large for current usage")

        return {
            "current_stats": stats,
            "recommendations": recommendations,
            "timestamp": datetime.utcnow().isoformat()
        }

# Global monitor instance
pool_monitor = None

def init_pool_monitor(engine):
    """Initialize connection pool monitoring"""
    global pool_monitor
    pool_monitor = ConnectionPoolMonitor(engine)
    pool_monitor.start_monitoring()
    return pool_monitor

def shutdown_pool_monitor():
    """Shutdown connection pool monitoring"""
    global pool_monitor
    if pool_monitor:
        pool_monitor.stop_monitoring()
        pool_monitor = None
```

## Environment Setup Examples

### Docker Compose for Development
```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://username:password@neon-project.region.neon.tech:5432/dbname?sslmode=require
      - DATABASE_POOL_SIZE=5
      - DATABASE_MAX_OVERFLOW=10
      - DATABASE_POOL_TIMEOUT=30
      - DATABASE_RECYCLE_TIME=300
      - DEBUG=false
    depends_on:
      - postgres
    volumes:
      - .:/app

  migrate:
    build: .
    environment:
      - DATABASE_URL=postgresql://username:password@neon-project.region.neon.tech:5432/dbname?sslmode=require
    command: python scripts/manage_migrations.py run
    depends_on:
      - postgres
    volumes:
      - .:/app
```

### Environment Configuration for Different Stages
```python
# config/environments.py
import os
from typing import Dict

class EnvironmentConfig:
    """Configuration for different deployment environments"""

    @staticmethod
    def get_neon_config(environment: str) -> Dict[str, any]:
        """Get Neon configuration based on environment"""

        base_config = {
            "pool_size": 5,
            "max_overflow": 10,
            "pool_timeout": 30,
            "pool_recycle": 300,
            "pool_pre_ping": True
        }

        if environment == "development":
            dev_config = base_config.copy()
            dev_config.update({
                "echo": True,  # Enable SQL logging in development
                "pool_size": 2,  # Smaller pool for development
                "max_overflow": 5
            })
            return dev_config

        elif environment == "staging":
            staging_config = base_config.copy()
            staging_config.update({
                "pool_size": 3,
                "max_overflow": 8
            })
            return staging_config

        elif environment == "production":
            prod_config = base_config.copy()
            prod_config.update({
                "pool_size": 10,
                "max_overflow": 20,
                "pool_timeout": 60,
                "echo": False
            })
            return prod_config

        else:
            return base_config

# Usage in main configuration
def get_current_env_config():
    env = os.getenv("ENVIRONMENT", "development")
    return EnvironmentConfig.get_neon_config(env)
```