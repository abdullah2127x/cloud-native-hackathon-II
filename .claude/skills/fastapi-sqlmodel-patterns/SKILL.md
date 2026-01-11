---
name: fastapi-sqlmodel-patterns
description: |
  This skill should be used when creating FastAPI endpoints, SQLModel database models, or Pydantic schemas.
  Use when building REST APIs or defining database tables with FastAPI and SQLModel.
---

# FastAPI SQLModel Patterns Skill

Auto-invoke when creating FastAPI endpoints, SQLModel database models, or Pydantic schemas. Use when building REST APIs or defining database tables with FastAPI and SQLModel.

## SQLModel Model Definition Patterns

SQLModel combines Pydantic and SQLAlchemy features to create powerful data models. Here are the common patterns:

### Base Model (Shared Attributes)
```python
from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime

class BaseModel(SQLModel):
    """Base model containing shared attributes"""
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
```

### Main Model (Database Table)
```python
from sqlmodel import Field, SQLModel
from typing import Optional

class User(BaseModel, table=True):
    """Database model for users table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255)
    username: str = Field(unique=True, nullable=False, max_length=100)
    first_name: str = Field(nullable=False, max_length=100)
    last_name: str = Field(nullable=False, max_length=100)
    is_active: bool = Field(default=True)
    hashed_password: str = Field(nullable=False, max_length=255)

    # Relationship definitions can go here
    # todos: List["Todo"] = Relationship(back_populates="user")
```

### Create Schema (Input Validation)
```python
from pydantic import field_validator
import re

class UserCreate(BaseModel):
    """Schema for creating new users"""
    email: str
    username: str
    first_name: str
    last_name: str
    password: str

    @field_validator("email")
    def validate_email(cls, v):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError("Invalid email format")
        return v

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v
```

### Read Schema (Output Validation)
```python
from pydantic import computed_field

class UserRead(BaseModel):
    """Schema for returning user data"""
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    # Computed fields can be added here
    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
```

### Update Schema (Partial Updates)
```python
from typing import Optional

class UserUpdate(SQLModel):
    """Schema for updating user data (partial updates)"""
    email: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
```

## FastAPI Endpoint Structure with Async/Await

FastAPI endpoints should use async/await for optimal performance:

### Basic CRUD Endpoints
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models.user import User, UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=201)
async def create_user(user: UserCreate, session: Session = Depends(get_session)):
    """Create a new user"""
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_password = hash_password(user.password)

    # Create new user instance
    db_user = User(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, session: Session = Depends(get_session)):
    """Get a user by ID"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.get("/", response_model=List[UserRead])
async def get_users(
    offset: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Get all users with pagination"""
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: Session = Depends(get_session)
):
    """Update a user by ID"""
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update only provided fields
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@router.delete("/{user_id}")
async def delete_user(user_id: int, session: Session = Depends(get_session)):
    """Delete a user by ID"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()

    return {"message": "User deleted successfully"}
```

## Dependency Injection for Database Sessions

### Database Session Dependency
```python
from sqlmodel import create_engine, Session
from typing import Generator
from app.config import settings

# Create engine once and reuse
engine = create_engine(str(settings.DATABASE_URL))

def get_session() -> Generator[Session, None, None]:
    """Dependency to provide database session"""
    with Session(engine) as session:
        yield session
```

### Using Session in Endpoints
```python
from fastapi import Depends
from sqlmodel import Session

@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    session: Session = Depends(get_session)  # Inject session dependency
):
    # Use session to query database
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
```

## HTTPException for Error Responses

Proper error handling with appropriate HTTP status codes:

```python
from fastapi import HTTPException

# Common error patterns
def handle_not_found(item_type: str, item_id: int):
    """Raise 404 error for missing items"""
    raise HTTPException(
        status_code=404,
        detail=f"{item_type} with ID {item_id} not found"
    )

def handle_bad_request(detail: str):
    """Raise 400 error for bad requests"""
    raise HTTPException(
        status_code=400,
        detail=detail
    )

def handle_unauthorized(detail: str = "Not authorized"):
    """Raise 401 error for unauthorized access"""
    raise HTTPException(
        status_code=401,
        detail=detail
    )

def handle_forbidden(detail: str = "Access forbidden"):
    """Raise 403 error for forbidden access"""
    raise HTTPException(
        status_code=403,
        detail=detail
    )
```

### Example with Error Handling
```python
@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, session: Session = Depends(get_session)):
    """Get a user by ID with proper error handling"""
    try:
        user = session.get(User, user_id)
        if not user:
            handle_not_found("User", user_id)

        return user
    except Exception as e:
        # Log error and return appropriate response
        logger.error(f"Error retrieving user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

## Response Models and Status Codes

### Standard Response Models
```python
from pydantic import BaseModel

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str

class ItemDeletedResponse(BaseModel):
    """Response for deletion operations"""
    message: str
    deleted_id: int
```

### Status Code Guidelines
```python
from fastapi import status

# Common status codes for different operations
CREATE_STATUS = status.HTTP_201_CREATED      # For successful creation
OK_STATUS = status.HTTP_200_OK              # For successful requests
NO_CONTENT_STATUS = status.HTTP_204_NO_CONTENT  # For successful deletions
BAD_REQUEST_STATUS = status.HTTP_400_BAD_REQUEST  # For validation errors
UNAUTHORIZED_STATUS = status.HTTP_401_UNAUTHORIZED  # For auth errors
FORBIDDEN_STATUS = status.HTTP_403_FORBIDDEN  # For permission errors
NOT_FOUND_STATUS = status.HTTP_404_NOT_FOUND  # For missing resources
CONFLICT_STATUS = status.HTTP_409_CONFLICT    # For conflicts (e.g., duplicate email)
INTERNAL_ERROR_STATUS = status.HTTP_500_INTERNAL_SERVER_ERROR  # For server errors
```

### Using Status Codes in Endpoints
```python
from fastapi import status

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, session: Session = Depends(get_session)):
    """Create a new user with 201 status"""
    # Implementation here
    pass

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: Session = Depends(get_session)):
    """Delete a user with 204 status"""
    # Implementation here
    # Don't return anything for 204 status codes
```

## Input Validation with Pydantic

Pydantic provides powerful validation capabilities:

### Field Validation
```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    priority: int = Field(ge=1, le=5)  # Greater than or equal to 1, less than or equal to 5
    is_completed: bool = False

    @field_validator("title")
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty or just whitespace")
        return v.title()  # Capitalize title

    @field_validator("priority")
    def priority_must_be_valid(cls, v):
        if v not in range(1, 6):  # 1 to 5
            raise ValueError("Priority must be between 1 and 5")
        return v
```

### Model Validation
```python
from pydantic import model_validator

class UserCreate(BaseModel):
    email: str
    password: str
    confirm_password: str

    @model_validator(mode='after')
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
```

## Database Session Management

### Session Dependency with Transaction Management
```python
from contextlib import contextmanager
from sqlmodel import Session, create_engine
from typing import Generator

engine = create_engine(str(settings.DATABASE_URL))

@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Context manager for database sessions with automatic rollback on error"""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Alternative dependency injection approach
def get_session() -> Generator[Session, None, None]:
    """Dependency to provide database session with automatic cleanup"""
    with Session(engine) as session:
        yield session
```

### Transaction Management in Endpoints
```python
@router.post("/transfer")
async def transfer_funds(
    transfer_data: TransferCreate,
    session: Session = Depends(get_session)
):
    """Transfer funds between accounts with transaction management"""
    try:
        # Get sender account
        sender = session.get(Account, transfer_data.sender_id)
        if not sender:
            raise HTTPException(status_code=404, detail="Sender account not found")

        # Get receiver account
        receiver = session.get(Account, transfer_data.receiver_id)
        if not receiver:
            raise HTTPException(status_code=404, detail="Receiver account not found")

        # Check balance
        if sender.balance < transfer_data.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")

        # Perform transfer
        sender.balance -= transfer_data.amount
        receiver.balance += transfer_data.amount

        # Add transaction records
        sender_transaction = Transaction(
            account_id=sender.id,
            amount=-transfer_data.amount,
            transaction_type="transfer_out"
        )
        receiver_transaction = Transaction(
            account_id=receiver.id,
            amount=transfer_data.amount,
            transaction_type="transfer_in"
        )

        session.add(sender_transaction)
        session.add(receiver_transaction)
        session.add(sender)
        session.add(receiver)

        session.commit()

        return {"message": "Transfer completed successfully"}
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Transfer failed")
```

## Query Patterns with SQLModel Select()

### Basic Queries
```python
from sqlmodel import select

# Get single record
user = session.exec(select(User).where(User.id == user_id)).first()

# Get all records with filters
users = session.exec(select(User).where(User.is_active == True)).all()

# Get with ordering
users = session.exec(
    select(User).order_by(User.created_at.desc())
).all()

# Get with limit and offset (pagination)
users = session.exec(
    select(User).offset(skip).limit(limit)
).all()
```

### Advanced Queries
```python
# Join queries
from sqlmodel import select
from sqlalchemy.orm import joinedload

# Using relationships (if defined)
users_with_todos = session.exec(
    select(User).options(joinedload(User.todos))
).all()

# Complex filtering
active_users_with_recent_activity = session.exec(
    select(User)
    .where(User.is_active == True)
    .where(User.updated_at >= datetime.utcnow() - timedelta(days=7))
    .order_by(User.updated_at.desc())
).all()

# Aggregation queries
from sqlalchemy import func

user_count = session.exec(
    select(func.count(User.id))
    .where(User.is_active == True)
).one()
```

### Pagination Helper
```python
from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    offset: int
    limit: int

def paginate_query(session, query, offset: int, limit: int, model_class):
    """Helper function for paginated queries"""
    # Get total count
    count_query = query
    total = session.exec(select(func.count()).select_from(count_query.subquery())).one()

    # Get paginated results
    items = session.exec(query.offset(offset).limit(limit)).all()

    return PaginatedResponse(
        items=items,
        total=total,
        offset=offset,
        limit=limit
    )

# Usage in endpoint
@router.get("/", response_model=PaginatedResponse[UserRead])
async def get_users_paginated(
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session)
):
    query = select(User)
    return paginate_query(session, query, offset, limit, User)
```

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing FastAPI project structure, SQLModel models, API patterns, database configuration |
| **Conversation** | User's specific requirements for endpoints, models, or validation rules |
| **Skill References** | FastAPI and SQLModel patterns from `references/` (models, endpoints, validation, etc.) |
| **User Guidelines** | Project-specific conventions, team standards, security requirements |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).