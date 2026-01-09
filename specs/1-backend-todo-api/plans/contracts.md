# API Contracts: Backend Todo API

**Feature**: 1-backend-todo-api
**Created**: 2026-01-08
**Status**: Final

## Base URL
`/api/{user_id}/tasks`

## Authentication
All endpoints require a valid JWT token in the Authorization header:
`Authorization: Bearer <jwt_token>`

## Common Response Formats

### Success Response
```
{
  "success": true,
  "data": { ... },
  "timestamp": "2026-01-08T10:30:00.123Z"
}
```

### Error Response
```
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": { ... } // optional
  },
  "timestamp": "2026-01-08T10:30:00.123Z"
}
```

### Common Error Codes
- `AUTH_ERROR`: Invalid or expired authentication token
- `VALIDATION_ERROR`: Request validation failed
- `NOT_FOUND`: Resource not found
- `FORBIDDEN`: Access denied to resource
- `INTERNAL_ERROR`: Server error occurred

## Endpoints

### GET /api/{user_id}/tasks
**Description**: Retrieve all tasks for a specific user

**Path Parameters**:
- `user_id` (string): The ID of the user whose tasks to retrieve

**Query Parameters**:
- `completed` (string, optional): Filter by completion status ("true", "false")
- `limit` (integer, optional): Maximum number of results (default: 50, max: 100)
- `offset` (integer, optional): Number of results to skip (default: 0)

**Headers**:
- `Authorization: Bearer <token>`

**Responses**:
- `200 OK`: Successfully retrieved tasks
  ```
  {
    "success": true,
    "data": [
      {
        "id": 1,
        "title": "Sample task",
        "description": "Task description",
        "completed": false,
        "created_at": "2026-01-08T10:30:00.123Z",
        "updated_at": "2026-01-08T10:30:00.123Z",
        "user_id": "user-123"
      }
    ],
    "meta": {
      "total": 1,
      "limit": 50,
      "offset": 0
    },
    "timestamp": "2026-01-08T10:30:00.123Z"
  }
  ```
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User attempting to access another user's tasks
- `404 Not Found`: User ID does not exist

### POST /api/{user_id}/tasks
**Description**: Create a new task for a specific user

**Path Parameters**:
- `user_id` (string): The ID of the user to create task for

**Headers**:
- `Authorization: Bearer <token>`

**Request Body**:
```
{
  "title": "Task title (required)",
  "description": "Task description (optional)"
}
```

**Responses**:
- `201 Created`: Task successfully created
  ```
  {
    "success": true,
    "data": {
      "id": 1,
      "title": "Task title",
      "description": "Task description",
      "completed": false,
      "created_at": "2026-01-08T10:30:00.123Z",
      "updated_at": "2026-01-08T10:30:00.123Z",
      "user_id": "user-123"
    },
    "timestamp": "2026-01-08T10:30:00.123Z"
  }
  ```
- `400 Bad Request`: Validation error
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User attempting to create task for another user

### GET /api/{user_id}/tasks/{id}
**Description**: Retrieve a specific task for a user

**Path Parameters**:
- `user_id` (string): The ID of the user
- `id` (integer): The ID of the task

**Headers**:
- `Authorization: Bearer <token>`

**Responses**:
- `200 OK`: Task successfully retrieved
  ```
  {
    "success": true,
    "data": {
      "id": 1,
      "title": "Task title",
      "description": "Task description",
      "completed": false,
      "created_at": "2026-01-08T10:30:00.123Z",
      "updated_at": "2026-01-08T10:30:00.123Z",
      "user_id": "user-123"
    },
    "timestamp": "2026-01-08T10:30:00.123Z"
  }
  ```
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User attempting to access another user's task
- `404 Not Found`: Task or user not found

### PUT /api/{user_id}/tasks/{id}
**Description**: Update a specific task for a user

**Path Parameters**:
- `user_id` (string): The ID of the user
- `id` (integer): The ID of the task

**Headers**:
- `Authorization: Bearer <token>`

**Request Body**:
```
{
  "title": "Updated task title (required)",
  "description": "Updated task description (optional)"
}
```

**Responses**:
- `200 OK`: Task successfully updated
  ```
  {
    "success": true,
    "data": {
      "id": 1,
      "title": "Updated task title",
      "description": "Updated task description",
      "completed": false,
      "created_at": "2026-01-08T10:30:00.123Z",
      "updated_at": "2026-01-08T10:30:00.123Z",
      "user_id": "user-123"
    },
    "timestamp": "2026-01-08T10:30:00.123Z"
  }
  ```
- `400 Bad Request`: Validation error
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User attempting to update another user's task
- `404 Not Found`: Task or user not found

### DELETE /api/{user_id}/tasks/{id}
**Description**: Delete a specific task for a user

**Path Parameters**:
- `user_id` (string): The ID of the user
- `id` (integer): The ID of the task

**Headers**:
- `Authorization: Bearer <token>`

**Responses**:
- `204 No Content`: Task successfully deleted
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User attempting to delete another user's task
- `404 Not Found`: Task or user not found

### PATCH /api/{user_id}/tasks/{id}/complete
**Description**: Update the completion status of a specific task

**Path Parameters**:
- `user_id` (string): The ID of the user
- `id` (integer): The ID of the task

**Headers**:
- `Authorization: Bearer <token>`

**Request Body**:
```
{
  "completed": true
}
```

**Responses**:
- `200 OK`: Task completion status successfully updated
  ```
  {
    "success": true,
    "data": {
      "id": 1,
      "title": "Task title",
      "description": "Task description",
      "completed": true,
      "created_at": "2026-01-08T10:30:00.123Z",
      "updated_at": "2026-01-08T10:30:00.123Z",
      "user_id": "user-123"
    },
    "timestamp": "2026-01-08T10:30:00.123Z"
  }
  ```
- `400 Bad Request`: Validation error (invalid completed value)
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User attempting to update another user's task
- `404 Not Found`: Task or user not found

## Validation Rules

### Request Validation
- All string fields trimmed of leading/trailing whitespace
- Title: 1-100 characters
- Description: 0-1000 characters if provided
- user_id in path must match authenticated user
- completed field must be boolean if provided

### Response Validation
- All timestamps in ISO 8601 format
- Success responses always include success: true
- Error responses always include success: false and error object
- Data field only present in successful responses

## Security Considerations
- All endpoints require authentication
- User ID in path parameter is validated against authenticated user
- No user enumeration via timing attacks
- Input sanitization applied to prevent injection