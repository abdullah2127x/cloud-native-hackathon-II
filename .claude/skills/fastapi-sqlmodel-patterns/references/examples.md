# FastAPI SQLModel Patterns - Additional Examples

## Complete Example: Todo Application

### Database Models
```python
# models/todo.py
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime
import enum

class Priority(enum.IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

class Status(enum.IntEnum):
    TODO = 1
    IN_PROGRESS = 2
    DONE = 3

class TodoBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Priority = Field(default=Priority.MEDIUM)
    status: Status = Field(default=Status.TODO)
    due_date: Optional[datetime] = Field(default=None)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Todo(TodoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")

    # Relationship to user
    user: "User" = Relationship(back_populates="todos")

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)
    username: str = Field(unique=True, nullable=False, max_length=100)
    first_name: str = Field(nullable=False, max_length=100)
    last_name: str = Field(nullable=False, max_length=100)
    is_active: bool = Field(default=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False, max_length=255)

    # Relationship to todos
    todos: List[Todo] = Relationship(back_populates="user")
```

### Pydantic Schemas
```python
# schemas/todo.py
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from models.todo import Priority, Status

class TodoCreate(TodoBase):
    user_id: int

    @field_validator("title")
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

class TodoRead(TodoBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

class TodoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Priority] = None
    status: Optional[Status] = None
    due_date: Optional[datetime] = None

class UserCreate(UserBase):
    password: str

    @field_validator("email")
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v

class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

class UserUpdate(SQLModel):
    email: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
```

### FastAPI Endpoints
```python
# api/todos.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, and_
from typing import List
from datetime import datetime
from database.session import get_session
from models.todo import Todo, User
from schemas.todo import TodoCreate, TodoRead, TodoUpdate

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("/", response_model=TodoRead, status_code=201)
async def create_todo(
    todo: TodoCreate,
    session: Session = Depends(get_session)
):
    # Verify user exists
    user = session.get(User, todo.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_todo = Todo.model_validate(todo)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo

@router.get("/", response_model=List[TodoRead])
async def get_todos(
    user_id: Optional[int] = Query(None),
    status: Optional[Status] = Query(None),
    priority: Optional[Priority] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session)
):
    query = select(Todo)

    # Apply filters
    if user_id:
        query = query.where(Todo.user_id == user_id)
    if status:
        query = query.where(Todo.status == status)
    if priority:
        query = query.where(Todo.priority == priority)

    # Apply pagination
    query = query.offset(offset).limit(limit).order_by(Todo.created_at.desc())

    todos = session.exec(query).all()
    return todos

@router.get("/{todo_id}", response_model=TodoRead)
async def get_todo(
    todo_id: int,
    session: Session = Depends(get_session)
):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo

@router.put("/{todo_id}", response_model=TodoRead)
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    session: Session = Depends(get_session)
):
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Update only provided fields
    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)

    db_todo.updated_at = datetime.utcnow()
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo

@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: int,
    session: Session = Depends(get_session)
):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    session.delete(todo)
    session.commit()

    return {"message": "Todo deleted successfully"}
```

## Authentication Example
```python
# auth/auth_handler.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from config.settings import settings

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.get(User, user_id)
    if user is None:
        raise credentials_exception
    return user
```

## Advanced Query Patterns

### Complex Joins and Filtering
```python
# Advanced queries with joins
from sqlmodel import select
from sqlalchemy import func

# Get user with their todo counts
def get_users_with_todo_counts(session: Session):
    query = (
        select(
            User,
            func.count(Todo.id).label('todo_count')
        )
        .join(Todo, User.id == Todo.user_id, isouter=True)
        .group_by(User.id)
        .order_by(func.count(Todo.id).desc())
    )
    results = session.exec(query).all()
    return results

# Get overdue todos with user info
def get_overdue_todos(session: Session):
    from datetime import datetime
    now = datetime.utcnow()

    query = (
        select(Todo, User)
        .join(User)
        .where(Todo.due_date < now)
        .where(Todo.status != Status.DONE)
        .order_by(Todo.due_date.asc())
    )
    results = session.exec(query).all()
    return results
```

### Batch Operations
```python
# Batch update endpoint
@router.patch("/batch-update")
async def batch_update_todos(
    todo_ids: List[int],
    update_data: TodoUpdate,
    session: Session = Depends(get_session)
):
    # Get all todos to update
    todos = session.exec(select(Todo).where(Todo.id.in_(todo_ids))).all()

    if not todos:
        raise HTTPException(status_code=404, detail="No todos found")

    # Update each todo
    update_dict = update_data.model_dump(exclude_unset=True)
    for todo in todos:
        for key, value in update_dict.items():
            setattr(todo, key, value)
        todo.updated_at = datetime.utcnow()
        session.add(todo)

    session.commit()

    return {"message": f"Updated {len(todos)} todos", "updated_ids": todo_ids}
```

## Background Tasks Example
```python
# Background tasks with FastAPI
from fastapi import BackgroundTasks
import asyncio

async def send_notification_email(todo_id: int, user_email: str):
    """Background task to send notification email"""
    # Simulate sending email
    await asyncio.sleep(1)  # Simulate network delay
    print(f"Notification sent for todo {todo_id} to {user_email}")

@router.post("/{todo_id}/complete", response_model=TodoRead)
async def complete_todo(
    todo_id: int,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.status = Status.DONE
    todo.updated_at = datetime.utcnow()

    session.add(todo)
    session.commit()
    session.refresh(todo)

    # Send notification in background
    user = session.get(User, todo.user_id)
    background_tasks.add_task(send_notification_email, todo.id, user.email)

    return todo
```