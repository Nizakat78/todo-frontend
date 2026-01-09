from sqlmodel import SQLModel, Field, create_engine, Session
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator
import html
import re
import uuid

# User Models
class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    name: Optional[str] = Field(default=None, max_length=100)
    password: str  # In real app, store hashed password

class User(UserBase, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    email: str
    name: Optional[str] = None
    password: str

    @validator('email')
    def validate_email(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Email cannot be empty')
        if '@' not in v:
            raise ValueError('Invalid email format')
        if len(v) > 255:
            raise ValueError('Email must be at most 255 characters')
        return v.strip()

    @validator('password')
    def validate_password(cls, v):
        if not v or len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        if len(v) > 128:
            raise ValueError('Password must be at most 128 characters')
        return v

class UserLogin(BaseModel):
    email: str
    password: str

    @validator('email')
    def validate_email(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Email cannot be empty')
        if '@' not in v:
            raise ValueError('Invalid email format')
        if len(v) > 255:
            raise ValueError('Email must be at most 255 characters')
        return v.strip()

    @validator('password')
    def validate_password(cls, v):
        if not v or len(v) < 1:
            raise ValueError('Password cannot be empty')
        if len(v) > 128:
            raise ValueError('Password must be at most 128 characters')
        return v

class UserResponse(BaseModel):
    success: bool
    data: dict
    token: str
    timestamp: str

# Task Models
class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: str  # From Better Auth

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

    @validator('title')
    def validate_title(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Title cannot be empty')
        if len(v) > 100:
            raise ValueError('Title must be at most 100 characters')
        # Sanitize input to prevent XSS
        sanitized = html.escape(v.strip())
        return sanitized

    @validator('description')
    def validate_description(cls, v):
        if v is not None and len(v) > 1000:
            raise ValueError('Description must be at most 1000 characters')
        # Sanitize input to prevent XSS
        if v:
            sanitized = html.escape(v.strip())
            return sanitized
        return v

class TaskUpdate(BaseModel):
    title: str
    description: Optional[str] = None

    @validator('title')
    def validate_title(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Title cannot be empty')
        if len(v) > 100:
            raise ValueError('Title must be at most 100 characters')
        # Sanitize input to prevent XSS
        sanitized = html.escape(v.strip())
        return sanitized

    @validator('description')
    def validate_description(cls, v):
        if v is not None and len(v) > 1000:
            raise ValueError('Description must be at most 1000 characters')
        # Sanitize input to prevent XSS
        if v:
            sanitized = html.escape(v.strip())
            return sanitized
        return v

class TaskResponse(BaseModel):
    success: bool
    data: Task
    timestamp: str

class TaskListResponse(BaseModel):
    success: bool
    data: list[Task]
    meta: dict
    timestamp: str