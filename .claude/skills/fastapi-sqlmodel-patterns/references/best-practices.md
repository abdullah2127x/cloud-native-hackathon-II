# FastAPI SQLModel Patterns - Best Practices and Common Patterns

## Model Design Best Practices

### ✅ DO: Separate Concerns with Different Model Classes
Create separate models for different purposes to maintain clean separation of concerns:

```python
# Good: Different models for different purposes
class UserBase(SQLModel):
    """Shared attributes for all user models"""
    email: str = Field(unique=True, nullable=False)
    username: str = Field(unique=True, nullable=False)

class User(UserBase, table=True):
    """Database model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = True

class UserCreate(UserBase):
    """Schema for creating users"""
    password: str

class UserRead(UserBase):
    """Schema for reading users"""
    id: int
    is_active: bool

class UserUpdate(SQLModel):
    """Schema for updating users (partial updates)"""
    email: Optional[str] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None
```

### ❌ AVOID: Single Model for All Operations
```python
# Avoid: Single model for everything
class User(SQLModel, table=True):
    """This tries to be everything at once"""
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False)
    username: str = Field(unique=True, nullable=False)
    password: str  # Should be hashed_password for DB, plain text for creation
    is_active: bool = True

    # This creates confusion about which fields are required for what operation
```

## Database Session Management Best Practices

### ✅ DO: Use Context Managers for Session Management
```python
# Good: Context manager for session management
from contextlib import contextmanager
from sqlmodel import Session

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
```

### ✅ DO: Use FastAPI Dependency Injection for Sessions
```python
# Good: Dependency injection for session management
def get_session() -> Generator[Session, None, None]:
    """Dependency to provide database session with automatic cleanup"""
    with Session(engine) as session:
        yield session

# Use in endpoints
@router.get("/{user_id}")
async def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

## Error Handling Best Practices

### ✅ DO: Create Reusable Error Handlers
```python
# Good: Reusable error handlers
def handle_not_found(model_name: str, id_value: int):
    """Standard 404 handler"""
    raise HTTPException(
        status_code=404,
        detail=f"{model_name} with ID {id_value} not found"
    )

def handle_conflict(model_name: str, field: str, value: str):
    """Standard 409 conflict handler"""
    raise HTTPException(
        status_code=409,
        detail=f"{model_name} with {field} '{value}' already exists"
    )

def handle_validation_error(detail: str):
    """Standard 422 validation error handler"""
    raise HTTPException(
        status_code=422,
        detail=detail
    )
```

### ✅ DO: Use Specific HTTP Status Codes
```python
from fastapi import status

# Good: Use appropriate status codes
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, session: Session = Depends(get_session)):
    # Create user
    pass

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: Session = Depends(get_session)):
    # Delete user
    pass
    # Return nothing for 204 status
```

## Validation Best Practices

### ✅ DO: Use Pydantic Validators
```python
# Good: Comprehensive validation
class UserCreate(BaseModel):
    email: str
    password: str
    age: int

    @field_validator("email")
    def validate_email_format(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v.lower()

    @field_validator("password")
    def validate_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain digit")
        return v

    @field_validator("age")
    def validate_age_range(cls, v):
        if v < 13:
            raise ValueError("Age must be at least 13")
        if v > 120:
            raise ValueError("Age must be less than 120")
        return v
```

### ✅ DO: Use Model Validators for Cross-Field Validation
```python
# Good: Cross-field validation
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

## Query Optimization Best Practices

### ✅ DO: Use Proper Indexing and Filtering
```python
# Good: Efficient querying with proper indexing
from sqlmodel import Field, create_index

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False, sa_column_kwargs={"index": True})
    username: str = Field(unique=True, nullable=False, sa_column_kwargs={"index": True})
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"index": True})

# Create composite indexes when needed
from sqlalchemy import Index

# This would be added to the table metadata
Index("idx_user_email_username", User.email, User.username)
```

### ✅ DO: Implement Proper Pagination
```python
# Good: Pagination with proper limits
async def get_items_paginated(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),  # Reasonable limits
    session: Session = Depends(get_session)
):
    items = session.exec(
        select(Item)
        .offset(offset)
        .limit(limit)
    ).all()

    # Get total count separately for pagination info
    total = session.exec(select(func.count(Item.id))).one()

    return {
        "items": items,
        "total": total,
        "offset": offset,
        "limit": limit
    }
```

## Security Best Practices

### ✅ DO: Hash Passwords Properly
```python
# Good: Proper password hashing
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Use in your models
class UserCreate(BaseModel):
    email: str
    password: str

    def hash_password(self):
        return hash_password(self.password)
```

### ✅ DO: Protect Sensitive Data in Responses
```python
# Good: Exclude sensitive fields from responses
class UserRead(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime

    # Never return password hashes in responses
    class Config:
        exclude = {"hashed_password"}

# Or use Pydantic's field exclusion
class UserRead(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    hashed_password: str = Field(exclude=True)
```

## Performance Optimization Patterns

### ✅ DO: Use Selective Field Loading
```python
# Good: Only select needed fields
async def get_user_summary(user_id: int, session: Session = Depends(get_session)):
    # Only select specific columns instead of entire row
    result = session.exec(
        select(User.id, User.email, User.username, User.created_at)
        .where(User.id == user_id)
    ).first()

    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    return result
```

### ✅ DO: Implement Caching for Expensive Queries
```python
# Good: Cache expensive queries
from functools import lru_cache

@lru_cache(maxsize=128)
def get_cached_user_stats(user_id: int):
    # Expensive calculation that benefits from caching
    pass

# Or use FastAPI's cache dependency
from starlette.concurrency import run_in_threadpool

async def get_cached_expensive_data():
    return await run_in_threadpool(expensive_calculation)
```

## Common Anti-Patterns to Avoid

### ❌ Anti-pattern: Fetching Entire Tables Without Limits
```python
# Avoid: Fetching all records without pagination
@router.get("/")
async def get_all_users(session: Session = Depends(get_session)):
    # This could crash your app with large datasets
    users = session.exec(select(User)).all()  # NO LIMIT!
    return users
```

### ✅ Solution: Always Use Pagination
```python
# Good: Always implement pagination
@router.get("/")
async def get_users(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: Session = Depends(get_session)
):
    users = session.exec(
        select(User)
        .offset(offset)
        .limit(limit)
    ).all()
    return users
```

### ❌ Anti-pattern: Exposing Raw Database Exceptions
```python
# Avoid: Letting raw database errors bubble up
@router.post("/")
async def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = User(email=user.email, username=user.username, hashed_password=hash_password(user.password))
    session.add(db_user)
    session.commit()  # This might raise raw database exception
    session.refresh(db_user)
    return db_user
```

### ✅ Solution: Handle Database Exceptions Properly
```python
# Good: Handle database exceptions gracefully
from sqlalchemy.exc import IntegrityError

@router.post("/")
async def create_user(user: UserCreate, session: Session = Depends(get_session)):
    try:
        db_user = User(
            email=user.email,
            username=user.username,
            hashed_password=hash_password(user.password)
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="User with this email or username already exists")
```

## Testing Best Practices

### ✅ DO: Create Test-Specific Models
```python
# Good: Test-specific models that inherit from main models
class UserCreateTest(UserCreate):
    """Test-specific model with relaxed validation if needed"""
    pass

# Use factories for creating test data
from factory import SQLModelFactory

class UserFactory(SQLModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"user{n}")
    is_active = True
```

## Async/Await Best Practices

### ✅ DO: Use Async Functions Appropriately
```python
# Good: Use async for I/O-bound operations
@router.get("/{user_id}")
async def get_user(user_id: int, session: Session = Depends(get_session)):
    # This is I/O bound (database query), so async makes sense
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# For CPU-bound operations, use run_in_threadpool
import asyncio

async def cpu_intensive_task():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, heavy_computation)
    return result
```