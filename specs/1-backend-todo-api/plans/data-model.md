# Data Model: Backend Todo API

**Feature**: 1-backend-todo-api
**Created**: 2026-01-08
**Status**: Final

## Entities

### Task Entity

**Description**: Represents a user's todo item with properties like title, description, completion status, and timestamps.

**Fields**:
- `id`: Integer (Primary Key, Auto-increment)
- `title`: String(100), Required
- `description`: Text, Optional (max 1000 characters)
- `completed`: Boolean, Default: False
- `created_at`: DateTime, Auto-populated
- `updated_at`: DateTime, Auto-populated
- `user_id`: String/UUID, Required (references external Better Auth user)

**Constraints**:
- `title` must not be empty
- `title` length ≤ 100 characters
- `description` length ≤ 1000 characters if provided
- `user_id` must match the authenticated user for access

**Indexes**:
- Primary: `id`
- Composite: `user_id` + `completed` (for efficient filtering)
- Single: `user_id` (for user-specific queries)

**Relationships**:
- Belongs to: User (via `user_id` foreign key, external to this application)

**State Transitions**:
- `completed` can transition from False → True or True → False
- All other fields can be updated except `id` and `created_at`

### Database Schema (SQLModel)

```python
from sqlmodel import SQLModel, Field, create_engine, Session
from datetime import datetime
from typing import Optional

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: str  # From Better Auth

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Update updated_at on modification
    def __setattr__(self, name, value):
        if name == 'updated_at':
            super().__setattr__('updated_at', datetime.utcnow())
        super().__setattr__(name, value)
```

## Validation Rules

### Input Validation
- `title`: Required, 1-100 characters, no leading/trailing whitespace
- `description`: Optional, 0-1000 characters
- `completed`: Boolean, default False
- `user_id`: String, validated against authenticated user

### Business Logic Validation
- Users can only access tasks where `user_id` matches their authenticated ID
- Users can only modify tasks they own
- Task creation requires valid authentication token

## Access Control
- Read: User must own the task (user_id matches authenticated user)
- Write: User must own the task (user_id matches authenticated user)
- Delete: User must own the task (user_id matches authenticated user)

## Data Integrity
- Foreign key constraint on `user_id` (referencing Better Auth user)
- Not-null constraints on required fields
- Length constraints on text fields
- Default values for `completed`, `created_at`, `updated_at`