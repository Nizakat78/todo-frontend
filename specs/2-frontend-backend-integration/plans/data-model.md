# Data Model: Frontend & Backend Integration

**Feature**: 2-frontend-backend-integration
**Created**: 2026-01-08
**Status**: Final

## Entities

### Task Entity (Backend)

**Description**: Represents a user's todo item that can be created, read, updated, and deleted through the integrated system.

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
- Belongs to: User (via `user_id` foreign key, external to our application)

### User Identity (JWT Claims)

**Description**: User identity information extracted from JWT token issued by Better Auth.

**Claims**:
- `sub`: String, Required (contains user ID)
- `exp`: Integer, Required (expiry timestamp)
- `iat`: Integer, Required (issued at timestamp)
- `iss`: String, Optional (issuer)

**Validation**:
- `sub` claim must be present and non-empty
- `exp` must be in the future
- Signature must be valid against BETTER_AUTH_SECRET

### API Response Format

**Description**: Standardized response format for all API endpoints to ensure frontend-backend consistency.

**Structure**:
```json
{
  "success": boolean,
  "data": any, // Present only on success
  "error": {
    "code": string,
    "message": string
  }, // Present only on error
  "timestamp": string // ISO format
}
```

### API Error Response Format

**Description**: Standardized error response format for all API endpoints.

**Structure**:
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  },
  "timestamp": "2026-01-08T10:30:00.123Z"
}
```

**Common Error Codes**:
- `AUTH_ERROR`: Invalid or expired authentication token
- `VALIDATION_ERROR`: Request validation failed
- `NOT_FOUND`: Resource not found
- `FORBIDDEN`: Access denied to resource
- `INTERNAL_ERROR`: Server error occurred

## Validation Rules

### Input Validation (Frontend → Backend)
- `title`: Required, 1-100 characters, no leading/trailing whitespace
- `description`: Optional, 0-1000 characters
- `completed`: Boolean, default False
- `user_id`: String, validated against authenticated user

### Business Logic Validation
- Users can only access tasks where `user_id` matches their authenticated ID
- Users can only modify tasks they own
- Task creation requires valid authentication token

### JWT Validation (Backend)
- Token signature must be valid against BETTER_AUTH_SECRET
- Token must not be expired (check `exp` claim)
- `sub` claim must be present and contain valid user ID

## Access Control
- Read: User must own the task (user_id matches authenticated user)
- Write: User must own the task (user_id matches authenticated user)
- Delete: User must own the task (user_id matches authenticated user)

## Data Flow Between Systems

### Frontend → Backend
1. Frontend retrieves JWT token from Better Auth
2. Frontend attaches token to Authorization header: `Bearer <token>`
3. Backend extracts user_id from JWT `sub` claim
4. Backend validates user_id matches URL parameter user_id
5. Backend filters database queries by user_id

### Backend → Frontend
1. Backend returns standardized response format
2. Frontend processes success/error responses consistently
3. Frontend updates UI based on response data
4. Frontend handles errors with appropriate user feedback