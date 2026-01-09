# Quickstart Guide: Frontend & Backend Integration

**Feature**: 2-frontend-backend-integration
**Created**: 2026-01-08
**Status**: Draft

## Integration Overview

This guide explains how to integrate the existing Next.js frontend with the FastAPI backend for secure, authenticated communication using JWT tokens from Better Auth.

## Prerequisites

- Frontend: Next.js application with Better Auth configured
- Backend: FastAPI server with JWT middleware and task endpoints
- Better Auth: JWT token generation and validation configured
- Shared secret: BETTER_AUTH_SECRET consistent between frontend and backend

## Environment Configuration

### Backend (.env)
```
BETTER_AUTH_SECRET=your-shared-secret-key
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
```

### Frontend (.env.local)
```
NEXT_PUBLIC_BETTER_AUTH_SECRET=your-shared-secret-key
NEXT_PUBLIC_BETTER_AUTH_API_URL=http://localhost:8000
```

## Integration Steps

### 1. Configure JWT Authentication Flow

The authentication flow works as follows:
1. User logs in through Better Auth
2. Better Auth issues JWT token
3. Frontend securely stores the token
4. Frontend attaches token to all API requests: `Authorization: Bearer <token>`
5. Backend validates JWT and extracts user identity
6. Backend enforces user isolation

### 2. Set Up Frontend API Client

Create a centralized API client that handles JWT attachment:

```typescript
// lib/api.ts
const apiClient = {
  get: async (url: string) => {
    const token = await getAuthToken(); // Retrieve from Better Auth
    return fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
  },

  post: async (url: string, data: any) => {
    const token = await getAuthToken();
    return fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
  },

  // Similar methods for put, delete, patch
};
```

### 3. Implement Backend JWT Middleware

The backend should validate JWT tokens and extract user identity:

```python
# utils/auth.py
def get_current_user(token: str = Security(security)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### 4. Verify User Isolation

Ensure all endpoints validate that the JWT user matches the URL parameter:

```python
# routes/tasks.py
@router.get("/tasks", ...)
async def get_tasks(user_id: str, current_user: str = Depends(get_current_user)):
    if user_id != current_user:
        raise HTTPException(status_code=403, detail="Not authorized")
    # Proceed with request
```

## API Endpoints Integration

### Available Endpoints
- `GET /api/{user_id}/tasks` - Get all tasks for user
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Update completion status

### Frontend Implementation
```typescript
// Example: Creating a task
const createTask = async (userId: string, taskData: TaskCreate) => {
  const response = await apiClient.post(`/api/${userId}/tasks`, taskData);
  const result = await response.json();

  if (!result.success) {
    throw new Error(result.error.message);
  }

  return result.data;
};
```

## Error Handling

### Frontend Error Handling
- Handle 401 responses by redirecting to login
- Handle 403 responses with appropriate user feedback
- Display user-friendly error messages
- Implement retry logic for network errors

### Backend Error Responses
- Return standardized error format
- Use appropriate HTTP status codes
- Include meaningful error messages
- Log security-related events

## Testing the Integration

### Authentication Test
1. Log in to the application
2. Verify JWT token is attached to API requests
3. Confirm backend validates token successfully

### CRUD Operations Test
1. Create a task through the frontend
2. Verify it's stored in the backend
3. Update the task and confirm changes are persisted
4. Delete the task and verify removal

### User Isolation Test
1. Log in as User A
2. Create a task
3. Attempt to access User B's tasks
4. Verify access is denied (403 response)

## Troubleshooting

### Common Issues
1. **Token not attaching to requests**: Check that JWT is properly retrieved from Better Auth
2. **401 Unauthorized errors**: Verify BETTER_AUTH_SECRET matches between frontend and backend
3. **403 Forbidden errors**: Ensure user_id in JWT matches URL parameter
4. **CORS errors**: Configure proper CORS settings for frontend domain

### Debugging Tips
- Enable logging on both frontend and backend
- Check JWT token format and validity
- Verify environment variables are set correctly
- Monitor network requests for proper headers