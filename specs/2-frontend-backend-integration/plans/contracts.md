# API Contracts: Frontend & Backend Integration

**Feature**: 2-frontend-backend-integration
**Created**: 2026-01-08
**Status**: Final

## Integration Overview

### Authentication Flow
1. User authenticates with Better Auth
2. Better Auth issues JWT token
3. Frontend stores JWT token securely
4. Frontend attaches JWT to all API requests: `Authorization: Bearer <token>`
5. Backend validates JWT signature and expiry
6. Backend extracts user_id from JWT `sub` claim
7. Backend compares JWT user_id with URL parameter user_id
8. Backend enforces user isolation

### Data Flow
- Frontend ↔ Backend: JSON payloads via HTTP/HTTPS
- Authentication: JWT tokens in Authorization header
- Error Handling: Standardized response format
- State Management: Backend as source of truth, Frontend for UI state

## Frontend API Client Interface

### Client Configuration
```typescript
interface ApiClientConfig {
  baseUrl: string;
  defaultHeaders: {
    'Content-Type': 'application/json';
    'Authorization': 'Bearer ${token}';
  };
}
```

### Request Format
- Headers: `Content-Type: application/json`, `Authorization: Bearer <token>`
- Body: JSON for POST/PUT/PATCH requests
- URL: `/api/${user_id}/tasks${path}` for all task operations

### Response Format
```typescript
interface ApiResponse<T> {
  success: boolean;
  data?: T;  // Present only on success
  error?: {
    code: string;
    message: string;
  };  // Present only on error
  timestamp: string;  // ISO format
}
```

## Backend API Contract

### Base URL
`/api/{user_id}/tasks`

### Authentication Requirements
All endpoints require a valid JWT token in the Authorization header:
`Authorization: Bearer <jwt_token>`

Backend performs these validations:
1. JWT signature verification against BETTER_AUTH_SECRET
2. Token expiry validation
3. User ID comparison: JWT `sub` claim vs URL parameter `user_id`
4. User isolation enforcement

### Common Response Formats

#### Success Response
```
{
  "success": true,
  "data": { ... },
  "timestamp": "2026-01-08T10:30:00.123Z"
}
```

#### Error Response
```
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
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

## Endpoint Specifications

### POST /api/{user_id}/tasks
**Description**: Create a new task for the authenticated user

**Request**:
- Headers: `Authorization: Bearer <token>`
- Body: `{title: string, description?: string}`
- Validation: JWT validity, user_id match, input validation

**Response**:
- `201 Created`: Task created successfully
- `400 Bad Request`: Validation error
- `401 Unauthorized`: Invalid/missing/expired token
- `403 Forbidden`: User_id mismatch (attempting to create for different user)

### GET /api/{user_id}/tasks
**Description**: Retrieve all tasks for the authenticated user

**Request**:
- Headers: `Authorization: Bearer <token>`
- Query params: `completed` (filter), `limit`, `offset` (pagination)
- Validation: JWT validity, user_id match

**Response**:
- `200 OK`: Tasks retrieved successfully
- `401 Unauthorized`: Invalid/missing/expired token
- `403 Forbidden`: User_id mismatch

### GET /api/{user_id}/tasks/{id}
**Description**: Retrieve a specific task for the authenticated user

**Request**:
- Headers: `Authorization: Bearer <token>`
- Validation: JWT validity, user_id match, task ownership

**Response**:
- `200 OK`: Task retrieved successfully
- `401 Unauthorized`: Invalid/missing/expired token
- `403 Forbidden`: User_id mismatch or task not owned by user
- `404 Not Found`: Task does not exist

### PUT /api/{user_id}/tasks/{id}
**Description**: Update a specific task for the authenticated user

**Request**:
- Headers: `Authorization: Bearer <token>`
- Body: `{title: string, description?: string}`
- Validation: JWT validity, user_id match, task ownership

**Response**:
- `200 OK`: Task updated successfully
- `400 Bad Request`: Validation error
- `401 Unauthorized`: Invalid/missing/expired token
- `403 Forbidden`: User_id mismatch or task not owned by user
- `404 Not Found`: Task does not exist

### DELETE /api/{user_id}/tasks/{id}
**Description**: Delete a specific task for the authenticated user

**Request**:
- Headers: `Authorization: Bearer <token>`
- Validation: JWT validity, user_id match, task ownership

**Response**:
- `204 No Content`: Task deleted successfully
- `401 Unauthorized`: Invalid/missing/expired token
- `403 Forbidden`: User_id mismatch or task not owned by user
- `404 Not Found`: Task does not exist

### PATCH /api/{user_id}/tasks/{id}/complete
**Description**: Update the completion status of a specific task

**Request**:
- Headers: `Authorization: Bearer <token>`
- Body: `{completed: boolean}`
- Validation: JWT validity, user_id match, task ownership

**Response**:
- `200 OK`: Completion status updated successfully
- `400 Bad Request`: Validation error
- `401 Unauthorized`: Invalid/missing/expired token
- `403 Forbidden`: User_id mismatch or task not owned by user
- `404 Not Found`: Task does not exist

## Integration Validation Points

### Frontend Responsibilities
1. Attach JWT token to all API requests
2. Handle 401 responses by redirecting to login
3. Handle 403 responses with appropriate user feedback
4. Parse standardized response format consistently
5. Update UI based on backend responses
6. Validate input before sending to backend

### Backend Responsibilities
1. Validate JWT token signature and expiry
2. Verify user_id in JWT matches URL parameter
3. Enforce user isolation for all operations
4. Return consistent response format
5. Properly set HTTP status codes
6. Validate all input from frontend

### Error Handling Contract
- Frontend must handle all HTTP error status codes appropriately
- Backend must return meaningful error messages in standard format
- Both sides must maintain consistent error categorization
- Network errors should have appropriate retry mechanisms

## Security Considerations
- All API calls require JWT authentication
- User isolation enforced at the backend level
- Input validation performed on backend
- JWT tokens validated with proper expiry checking
- Authorization checks performed for all operations