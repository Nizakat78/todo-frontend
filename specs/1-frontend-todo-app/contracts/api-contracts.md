# API Contracts: Frontend Todo Web App

## Overview
This document defines the API contracts that the frontend will use. Since this is a frontend-only implementation with placeholder API calls, these represent the expected interface that will be implemented when the backend is integrated.

## Authentication API

### POST /api/auth/login
**Description**: Authenticate user and return JWT token
**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200 OK)**:
```json
{
  "user": {
    "id": "user-123",
    "email": "user@example.com",
    "name": "John Doe",
    "createdAt": "2023-01-01T00:00:00Z"
  },
  "token": "jwt-token-string",
  "refreshToken": "refresh-token-string"
}
```

**Response (401 Unauthorized)**:
```json
{
  "error": "Invalid credentials",
  "message": "Email or password is incorrect"
}
```

### POST /api/auth/signup
**Description**: Create a new user account
**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Response (201 Created)**:
```json
{
  "user": {
    "id": "user-123",
    "email": "user@example.com",
    "name": "John Doe",
    "createdAt": "2023-01-01T00:00:00Z"
  },
  "token": "jwt-token-string",
  "refreshToken": "refresh-token-string"
}
```

**Response (409 Conflict)**:
```json
{
  "error": "Email already exists",
  "message": "An account with this email already exists"
}
```

### POST /api/auth/logout
**Description**: Logout user and invalidate token
**Headers**:
```
Authorization: Bearer {token}
```

**Response (200 OK)**:
```json
{
  "message": "Successfully logged out"
}
```

## Task API

### GET /api/tasks
**Description**: Get all tasks for the authenticated user
**Headers**:
```
Authorization: Bearer {token}
```

**Query Parameters**:
- `completed`: Optional filter ('true', 'false', or omitted for all)
- `sortBy`: Optional sort field ('created', 'updated', 'title') - default: 'created'
- `order`: Optional sort order ('asc', 'desc') - default: 'desc'
- `limit`: Optional limit number of results
- `offset`: Optional offset for pagination

**Response (200 OK)**:
```json
{
  "tasks": [
    {
      "id": "task-123",
      "title": "Complete project",
      "description": "Finish the todo app project",
      "completed": false,
      "createdAt": "2023-01-01T00:00:00Z",
      "updatedAt": "2023-01-01T00:00:00Z",
      "userId": "user-123"
    }
  ],
  "totalCount": 1,
  "hasMore": false
}
```

### GET /api/tasks/{id}
**Description**: Get a specific task by ID
**Headers**:
```
Authorization: Bearer {token}
```

**Response (200 OK)**:
```json
{
  "task": {
    "id": "task-123",
    "title": "Complete project",
    "description": "Finish the todo app project",
    "completed": false,
    "createdAt": "2023-01-01T00:00:00Z",
    "updatedAt": "2023-01-01T00:00:00Z",
    "userId": "user-123"
  }
}
```

**Response (404 Not Found)**:
```json
{
  "error": "Task not found",
  "message": "The requested task does not exist"
}
```

### POST /api/tasks
**Description**: Create a new task
**Headers**:
```
Authorization: Bearer {token}
```

**Request**:
```json
{
  "title": "New task",
  "description": "Task description",
  "completed": false
}
```

**Response (201 Created)**:
```json
{
  "task": {
    "id": "task-456",
    "title": "New task",
    "description": "Task description",
    "completed": false,
    "createdAt": "2023-01-01T00:00:00Z",
    "updatedAt": "2023-01-01T00:00:00Z",
    "userId": "user-123"
  },
  "message": "Task created successfully"
}
```

### PUT /api/tasks/{id}
**Description**: Update an existing task
**Headers**:
```
Authorization: Bearer {token}
```

**Request**:
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true
}
```

**Response (200 OK)**:
```json
{
  "task": {
    "id": "task-123",
    "title": "Updated task title",
    "description": "Updated task description",
    "completed": true,
    "createdAt": "2023-01-01T00:00:00Z",
    "updatedAt": "2023-01-02T00:00:00Z",
    "userId": "user-123"
  },
  "message": "Task updated successfully"
}
```

### DELETE /api/tasks/{id}
**Description**: Delete a task
**Headers**:
```
Authorization: Bearer {token}
```

**Response (200 OK)**:
```json
{
  "message": "Task deleted successfully"
}
```

**Response (404 Not Found)**:
```json
{
  "error": "Task not found",
  "message": "The requested task does not exist"
}
```

## Error Response Format
All error responses follow this format:
```json
{
  "error": "Error type",
  "message": "Human-readable error message",
  "statusCode": 400,
  "timestamp": "2023-01-01T00:00:00Z"
}
```

## Authentication Requirements
- All task-related endpoints require a valid JWT token in the Authorization header
- Authentication endpoints do not require tokens
- Invalid or expired tokens return 401 Unauthorized

## Placeholder Implementation Notes
For the frontend implementation phase:
- API responses should be mocked with realistic data
- Error responses should be simulated to test error handling
- Loading states should be implemented for all API calls
- The actual backend integration will replace these placeholder implementations