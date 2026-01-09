# Tasks: Backend Todo API Implementation

**Feature**: 1-backend-todo-api
**Created**: 2026-01-08
**Status**: Planned
**Author**: Claude

## Overview

Implementation of a FastAPI backend for the Todo application with JWT authentication, SQLModel ORM, and PostgreSQL database integration.

## Phase 1: Setup

### Goal
Initialize the project structure and dependencies needed for all subsequent phases.

### Tasks

- [x] T001 Create backend directory structure: `/backend/main.py`, `/backend/models.py`, `/backend/db.py`, `/backend/routes/tasks.py`, `/backend/utils/auth.py`, `/backend/utils/jwt_handler.py`
- [x] T002 Set up virtual environment and install dependencies: fastapi, sqlmodel, uvicorn, python-jose[cryptography], passlib[bcrypt], python-dotenv, psycopg2-binary
- [x] T003 Create requirements.txt with all project dependencies
- [x] T004 Create .env file with placeholder values for DATABASE_URL and BETTER_AUTH_SECRET
- [x] T005 Initialize main.py with basic FastAPI app and include router configuration

## Phase 2: Foundational Components

### Goal
Establish the foundational components that all user stories depend on: database connection, authentication, and error handling.

### Tasks

- [x] T006 [P] Create database connection module in `/backend/db.py` with engine, session, and initialization functions
- [x] T007 [P] Create Task model in `/backend/models.py` following the data model specification with proper fields and constraints
- [x] T008 [P] Implement JWT utility functions in `/backend/utils/jwt_handler.py` for encoding/decoding tokens
- [x] T009 [P] Create authentication dependency in `/backend/utils/auth.py` to validate JWT tokens
- [ ] T010 Create custom exception handlers for standardized error responses
- [x] T011 Implement database initialization and migration setup

## Phase 3: User Story 1 - Create New Tasks (Priority: P1)

### Goal
Enable users to create new tasks in their personal todo list.

### Independent Test Criteria
A user can successfully create a new task through the API, which gets stored in the database and is accessible only to that user.

### Tasks

- [x] T012 [US1] Create POST endpoint `/api/{user_id}/tasks` in `/backend/routes/tasks.py` with proper request validation
- [x] T013 [US1] Implement task creation logic with user_id validation to ensure user ownership
- [x] T014 [US1] Add input validation for task title (1-100 chars) and description (0-1000 chars)
- [x] T015 [US1] Implement proper response format with 201 status code for successful creation
- [x] T016 [US1] Add error handling for authentication failures (401) and validation errors (400)
- [x] T017 [US1] Add authorization check to ensure user can only create tasks for themselves

## Phase 4: User Story 2 - View Own Tasks (Priority: P1)

### Goal
Allow users to view all their tasks to manage and prioritize their work.

### Independent Test Criteria
A user can retrieve their own tasks through the API, seeing only tasks associated with their user ID.

### Tasks

- [x] T018 [US2] Create GET endpoint `/api/{user_id}/tasks` in `/backend/routes/tasks.py` with query parameter support
- [x] T019 [US2] Implement task retrieval logic with user_id validation to ensure user ownership
- [x] T020 [US2] Add support for query parameters: completed, limit, offset for pagination/filtering
- [x] T021 [US2] Implement proper response format with metadata for pagination
- [x] T022 [US2] Add error handling for authentication failures (401) and authorization errors (403)
- [x] T023 [US2] Add database query optimization with proper indexing for user_id and user_id+completed

## Phase 5: User Story 3 - Update Task Details (Priority: P2)

### Goal
Allow users to update their task details to modify priorities, descriptions, and other properties.

### Independent Test Criteria
A user can modify their own tasks through PUT requests, updating properties like title, description, or completion status.

### Tasks

- [x] T024 [US3] Create PUT endpoint `/api/{user_id}/tasks/{id}` in `/backend/routes/tasks.py` with proper request validation
- [x] T025 [US3] Implement task update logic with user_id and task ownership validation
- [x] T026 [US3] Add input validation for task title (1-100 chars) and description (0-1000 chars)
- [x] T027 [US3] Ensure only authorized users can update their own tasks
- [x] T028 [US3] Implement proper response format with 200 status code for successful updates
- [x] T029 [US3] Add error handling for authentication failures (401), authorization errors (403), and not found (404)

## Phase 6: User Story 4 - Delete Tasks (Priority: P2)

### Goal
Allow users to delete tasks that are no longer needed to keep their todo list clean.

### Independent Test Criteria
A user can remove their own tasks through DELETE requests, permanently removing them from the system.

### Tasks

- [x] T030 [US4] Create DELETE endpoint `/api/{user_id}/tasks/{id}` in `/backend/routes/tasks.py`
- [x] T031 [US4] Implement task deletion logic with user_id and task ownership validation
- [x] T032 [US4] Ensure only authorized users can delete their own tasks
- [x] T033 [US4] Implement proper response format with 204 No Content for successful deletion
- [x] T034 [US4] Add error handling for authentication failures (401), authorization errors (403), and not found (404)

## Phase 7: User Story 5 - Toggle Task Completion Status (Priority: P2)

### Goal
Allow users to mark tasks as complete/incomplete to track progress and prioritize active tasks.

### Independent Test Criteria
A user can update the completion status of their tasks through PATCH requests.

### Tasks

- [x] T035 [US5] Create PATCH endpoint `/api/{user_id}/tasks/{id}/complete` in `/backend/routes/tasks.py`
- [x] T036 [US5] Implement completion status update logic with user_id and task ownership validation
- [x] T037 [US5] Add input validation for completed field (must be boolean)
- [x] T038 [US5] Ensure only authorized users can update completion status of their tasks
- [x] T039 [US5] Implement proper response format with updated task data
- [x] T040 [US5] Add error handling for authentication failures (401), authorization errors (403), and not found (404)

## Phase 8: Error Handling & Validation Enhancement

### Goal
Implement comprehensive error handling and request validation across all endpoints.

### Tasks

- [x] T041 Create standardized error response format consistent across all endpoints
- [ ] T042 Implement centralized validation logic for common request parameters
- [ ] T043 Add database transaction handling for operations that modify data
- [x] T044 Implement proper logging for errors and security events
- [x] T045 Add input sanitization to prevent injection attacks
- [x] T046 Create comprehensive error documentation for API consumers

## Phase 9: Polish & Cross-Cutting Concerns

### Goal
Complete the implementation with documentation, testing, and configuration.

### Tasks

- [x] T047 Add comprehensive API documentation using FastAPI's automatic documentation
- [x] T048 Create README.md with setup instructions and API usage examples
- [x] T049 Implement basic unit tests for all API endpoints
- [x] T050 Add environment configuration for different deployment environments
- [ ] T051 Perform security review to ensure user isolation is properly enforced
- [ ] T052 Conduct integration testing for complete user workflows
- [ ] T053 Optimize database queries and add proper indexes based on access patterns
- [ ] T054 Final testing to ensure all success criteria are met

## Dependencies

- **Phase 2** depends on **Phase 1** completion
- **Phase 3-7** depend on **Phase 2** completion
- **Phase 8** depends on **Phase 3-7** completion
- **Phase 9** depends on **Phase 1-8** completion

## Parallel Execution Opportunities

- T006-T009 can run in parallel during Phase 2 (Foundational Components)
- T012-T017 (US1) can be developed independently from T018-T023 (US2), etc.
- Each user story phase can be worked on independently after Phase 2

## Implementation Strategy

1. **MVP First**: Complete Phase 1, 2, and US1 to have a minimal working version
2. **Incremental Delivery**: Add each user story as a complete, testable increment
3. **Security First**: Ensure user isolation is implemented correctly in all phases
4. **Test Continuously**: Validate each user story independently before moving to the next