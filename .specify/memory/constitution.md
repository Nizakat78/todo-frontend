<!-- Sync Impact Report:
Version change: N/A (initial creation) → 1.0.0
List of modified principles: N/A (new constitution)
Added sections: All sections (new constitution)
Removed sections: N/A
Templates requiring updates:
  - ✅ .specify/templates/plan-template.md (updated Constitution Check section)
  - ✅ .specify/templates/spec-template.md (aligned requirements sections)
  - ✅ .specify/templates/tasks-template.md (updated task categorization)
  - ✅ .specify/templates/commands/sp.constitution (no changes needed)
Follow-up TODOs: None
-->

# Phase II – Full-Stack Todo Web App Constitution

## Core Principles

### Spec-Driven Development (NON-NEGOTIABLE)
All implementation must follow Spec-Driven Development using Claude Code + Spec-Kit Plus; No manual code writing allowed - all code generation via spec prompts; Development follows strict sequence: spec → plan → tasks → implementation; Every feature requires complete specification before any coding begins.

### Modularity: Backend, Frontend, Integration Separation
Backend, Frontend, and Integration layers must be developed separately with clear boundaries; Each layer has independent testability and deployability; Clear API contracts between layers with versioning strategy; No cross-layer dependencies that violate architectural boundaries.

### Security: JWT-Based Authentication for Task Ownership
JWT-based authentication must protect all task endpoints and ensure user isolation; Each user must only see their own tasks with proper authorization checks; Authentication (Signup/Login) required for all task operations; Security must be implemented at both API and database levels.

### Clarity: Clean Code Structure and Readable Prompts
Code structure must be clean, well-organized, and maintainable with consistent patterns; All prompts and specifications must be readable and unambiguous; Documentation must be clear and comprehensive for all components; Code follows consistent naming and architectural patterns.

### Claude Code Mandate: All Code Generation via Claude Code
Claude Code must be used for ALL code generation - no manual coding allowed; All implementation must follow Claude Code workflows and templates; Human developers only provide specifications and validation; All code artifacts must be generated through Claude Code agents.

### Full-Stack Integration: Complete Frontend-Backend Functionality
Complete CRUD operations must work via both frontend and backend; Frontend Next.js App Router with Tailwind CSS must integrate seamlessly with FastAPI backend; All user interactions must flow through proper API endpoints; Complete end-to-end functionality required for each feature.

## Technology Stack Standards

### Backend Requirements
- REST API endpoints follow consistent patterns with proper HTTP methods and status codes
- Backend uses FastAPI + SQLModel for API development and database interaction
- Database uses Neon Serverless PostgreSQL for task persistence
- All endpoints must work with JWT token authentication and authorization
- Proper error handling, validation, and response formatting required

### Frontend Requirements
- Frontend uses Next.js App Router + Tailwind CSS for modern web development
- Responsive design that works across different screen sizes and devices
- All pages must be fully functional with proper state management
- Clean UI/UX with consistent styling and user experience
- Proper form handling, validation, and user feedback mechanisms

### Integration Standards
- User isolation enforced - each user sees only their own tasks
- Authentication (Signup/Login) must be fully functional
- Task CRUD operations (Add, Update, Delete, View, Mark Complete) must be complete
- Tasks must persist in database and be retrieved correctly
- Frontend and backend must communicate properly via API endpoints

## Development Workflow

### Implementation Requirements
- All endpoints and pages must work with JWT token authentication
- Task CRUD operations must be fully implemented with proper validation
- Authentication (Signup/Login) must be secure and functional
- Tasks must persist in database with proper data models
- Frontend must be responsive and fully functional
- Claude Code must be used for all code generation without exceptions

### Quality Gates
- All code must pass through Claude Code validation before acceptance
- End-to-end functionality must be tested before merging
- Database integration must be verified for data persistence
- Security requirements (JWT auth, user isolation) must be validated
- Frontend responsiveness and functionality must be confirmed
- API endpoints must follow consistent patterns and proper error handling

## Governance

All development must strictly adhere to this constitution. No code may be written manually - all implementation must be generated via Claude Code prompts. Changes to this constitution require explicit approval and must be documented as amendments. All pull requests and code reviews must verify compliance with these principles. The development sequence (spec → plan → tasks → implementation) must be strictly followed without deviation.

**Version**: 1.0.0 | **Ratified**: 2026-01-07 | **Last Amended**: 2026-01-07