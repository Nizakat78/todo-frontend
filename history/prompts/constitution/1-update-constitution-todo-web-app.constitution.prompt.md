---
id: 1
title: Update Constitution Todo Web App
stage: constitution
date: 2026-01-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 3-ai-robot-brain-module
user: user
command: sp.constitution
labels: [constitution,spec-driven-development,full-stack,todo-app]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests: []
---

## Prompt

```
text
Project: Phase II – Full-Stack Todo Web App

Core Principles:
- Spec-Driven Development (Claude Code + Spec-Kit Plus)
- No manual code writing; all implementation via spec prompts
- Modularity: Backend, Frontend, Integration separated
- Security: JWT-based authentication for task ownership
- Clarity: Clean code structure, readable prompts

Key Standards:
- REST API endpoints follow consistent patterns
- Frontend uses Next.js App Router + Tailwind CSS
- Backend uses FastAPI + SQLModel
- Database: Neon Serverless PostgreSQL
- User isolation enforced (each user sees own tasks)
- Spec reference: @specs/features/*.md for all features

Constraints:
- All endpoints and pages must work with JWT token
- Task CRUD (Add, Update, Delete, View, Mark Complete)
- Authentication (Signup/Login)
- Tasks persist in database
- Frontend responsive and functional
- Claude Code must be used for all code generation

Success Criteria:
- Full CRUD via frontend and backend
- JWT auth protects all task endpoints
- Frontend pages fully functional
- Database integration correct
- Specs fully implemented via Claude Code
```

## Response snapshot

Constitution file updated with new principles for the Phase II Full-Stack Todo Web App project, including:
- Spec-Driven Development (NON-NEGOTIABLE)
- Modularity: Backend, Frontend, Integration Separation
- Security: JWT-Based Authentication for Task Ownership
- Clarity: Clean Code Structure and Readable Prompts
- Claude Code Mandate: All Code Generation via Claude Code
- Full-Stack Integration: Complete Frontend-Backend Functionality

## Outcome

- ✅ Impact: Created project constitution with 6 core principles and detailed standards
- 🧪 Tests: No tests required for constitution creation
- 📁 Files: Updated .specify/memory/constitution.md with comprehensive project governance
- 🔁 Next prompts: Ready to proceed with spec creation using Claude Code
- 🧠 Reflection: Constitution aligns with spec-driven development requirements and enforces Claude Code usage

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable
- Prompt variant (if applicable): Not applicable
- Next experiment (smallest change to try): Proceed with feature specification