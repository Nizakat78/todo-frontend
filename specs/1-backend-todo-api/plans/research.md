# Research Document: Backend Todo API Implementation

**Feature**: 1-backend-todo-api
**Created**: 2026-01-08
**Status**: Completed

## RD-001: JWT Implementation Best Practices

**Decision**: Use HS256 algorithm with 15-minute access token expiration
**Rationale**: HS256 is simpler to implement and sufficient for web applications. 15-minute expiration balances security (short-lived tokens) with user experience (not requiring frequent re-authentication).
**Alternatives considered**:
- RS256: More complex key management, overkill for this application
- Longer expiration: Less secure, increases exposure window
- Shorter expiration: Better security but worse UX with frequent re-authentication

## RD-002: Task Field Validation Standards

**Decision**: Title max 100 characters, Description max 1000 characters, Title required, Description optional
**Rationale**: 100 characters is sufficient for task titles while preventing abuse. 1000 characters allows for detailed descriptions. Making title required ensures all tasks have identifying information.
**Alternatives considered**:
- Shorter limits: Might be restrictive for legitimate use cases
- Longer limits: Increases database storage and potential for abuse
- Both required: Description might not always be necessary

## RD-003: Error Response Format Patterns

**Decision**: Standardized error format with error_code, message, and timestamp
**Rationale**: Consistent error responses make client-side handling easier and provide debugging information.
**Format**: `{error_code: string, message: string, details?: object, timestamp: ISO_string}`
**Alternatives considered**:
- Minimal format: Less debugging info
- Extended format: Potentially exposing sensitive information

## RD-004: FastAPI Authentication Middleware Patterns

**Decision**: Global dependency injection with route-specific overrides
**Rationale**: Global authentication middleware reduces repetition while allowing specific routes to opt-out if needed. Dependency injection makes testing easier.
**Pattern**: Use Depends() for authentication in routes, with a global middleware for token extraction
**Alternatives considered**:
- Decorator pattern: More verbose, harder to maintain
- Manual checking in each route: Repetitive and error-prone

## RD-005: SQLModel Relationship Patterns

**Decision**: Foreign key relationship with user_id on Task model, no direct User model (will rely on Better Auth)
**Rationale**: Since user authentication is handled by Better Auth, we only need to store user_id in our Task model to enforce ownership. This avoids duplicating user data.
**Relationship**: Task.user_id → User.id (external to our application)
**Alternatives considered**:
- Full User model: Would duplicate data managed by Better Auth
- UUID keys: More complex but better for distributed systems (overkill for this application)