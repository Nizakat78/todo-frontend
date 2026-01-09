# Data Model: Frontend Todo Web App

## Key Entities

### User
**Description**: Represents a registered user with authentication credentials
**Fields**:
- `id`: string - Unique identifier for the user
- `email`: string - User's email address (used for login)
- `name?`: string - Optional user name
- `createdAt`: Date - Timestamp when the user account was created
- `updatedAt`: Date - Timestamp when the user account was last updated

**Validation Rules**:
- Email must be a valid email format
- Email must be unique
- Required fields: id, email, createdAt

### Task
**Description**: Represents a task with properties like title, description, status, and timestamps
**Fields**:
- `id`: string - Unique identifier for the task
- `title`: string - Title of the task
- `description`: string - Detailed description of the task
- `completed`: boolean - Status indicating if the task is completed
- `createdAt`: Date - Timestamp when the task was created
- `updatedAt`: Date - Timestamp when the task was last updated
- `userId`: string - Foreign key linking to the user who owns the task

**Validation Rules**:
- Title is required and must be 1-100 characters
- Description is optional and can be up to 1000 characters
- Completed defaults to false
- Required fields: id, title, completed, createdAt, userId

## State Transitions

### Task State Transitions
- **Active** → **Completed**: When user marks task as complete
- **Completed** → **Active**: When user marks task as incomplete

### User Authentication States
- **Logged Out** → **Logging In**: When user submits login form
- **Logging In** → **Logged In**: When login API call succeeds
- **Logging In** → **Login Failed**: When login API call fails
- **Logged In** → **Logged Out**: When user logs out

## Relationships
- **User → Task**: One-to-many (one user can have many tasks)
- **Task → User**: Many-to-one (many tasks belong to one user)

## API Response Structures

### Authentication Responses
**Login Success**:
```typescript
{
  user: User,
  token: string,
  refreshToken?: string
}
```

**Login Error**:
```typescript
{
  error: string,
  message: string
}
```

### Task API Responses
**Get Tasks Success**:
```typescript
{
  tasks: Task[],
  totalCount: number
}
```

**Get Task Success**:
```typescript
{
  task: Task
}
```

**Task Modification Success**:
```typescript
{
  task: Task,
  message: string
}
```

**Task Error**:
```typescript
{
  error: string,
  message: string
}
```

## Frontend State Structure

### Authentication State
```typescript
{
  user: User | null,
  token: string | null,
  isAuthenticated: boolean,
  isLoading: boolean,
  error: string | null
}
```

### Task State
```typescript
{
  tasks: Task[],
  currentTask: Task | null,
  isLoading: boolean,
  error: string | null,
  filters: {
    completed: 'all' | 'completed' | 'active',
    sortBy: 'created' | 'updated' | 'title'
  }
}
```