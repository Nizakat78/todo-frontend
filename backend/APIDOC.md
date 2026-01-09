# Todo API Documentation

## Base URL
`/api/{user_id}/tasks`

## Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Common Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "timestamp": "2026-01-08T10:30:00.123Z"
}
```

### Error Response
```json
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

### POST /api/{user_id}/tasks
Create a new task for the specified user.

**Path Parameters**:
- `user_id` (string): The ID of the user to create task for

**Headers**:
- `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "title": "Task title (required, 1-100 chars)",
  "description": "Task description (optional, max 1000 chars)"
}
```

**Responses**:
- `201 Created`: Task successfully created
- `400 Bad Request`: Validation error
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User attempting to create task for another user

### GET /api/{user_id}/tasks
Retrieve all tasks for a specific user.

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
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User attempting to access another user's tasks

### GET /api/{user_id}/tasks/{id}
Retrieve a specific task for a user.

**Path Parameters**:
- `user_id` (string): The ID of the user
- `id` (integer): The ID of the task

**Headers**:
- `Authorization: Bearer <token>`

**Responses**:
- `200 OK`: Task successfully retrieved
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User attempting to access another user's task
- `404 Not Found`: Task or user not found

### PUT /api/{user_id}/tasks/{id}
Update a specific task for a user.

**Path Parameters**:
- `user_id` (string): The ID of the user
- `id` (integer): The ID of the task

**Headers**:
- `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "title": "Updated task title (required, 1-100 chars)",
  "description": "Updated task description (optional, max 1000 chars)"
}
```

**Responses**:
- `200 OK`: Task successfully updated
- `400 Bad Request`: Validation error
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User attempting to update another user's task
- `404 Not Found`: Task or user not found

### DELETE /api/{user_id}/tasks/{id}
Delete a specific task for a user.

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
Update the completion status of a specific task.

**Path Parameters**:
- `user_id` (string): The ID of the user
- `id` (integer): The ID of the task

**Headers**:
- `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "completed": true
}
```

**Responses**:
- `200 OK`: Task completion status successfully updated
- `400 Bad Request`: Validation error (invalid completed value)
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User attempting to update another user's task
- `404 Not Found`: Task or user not found

## Security Considerations
- All endpoints require authentication
- User ID in path parameter is validated against authenticated user
- Input sanitization applied to prevent XSS attacks
- User isolation enforced - users can only access their own tasks