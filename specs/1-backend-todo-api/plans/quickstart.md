# Quickstart Guide: Backend Todo API

**Feature**: 1-backend-todo-api
**Created**: 2026-01-01
**Status**: Draft

## Prerequisites

- Python 3.8+
- pip package manager
- Virtual environment tool (venv, conda, etc.)
- PostgreSQL-compatible database (Neon Serverless recommended)
- Better Auth frontend setup completed

## Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install fastapi sqlmodel uvicorn python-jose[cryptography] passlib[bcrypt] python-dotenv httpx
```

### 4. Environment Configuration
Create a `.env` file in the backend directory:
```
DATABASE_URL=postgresql://username:password@host:port/database_name
BETTER_AUTH_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
```

### 5. Project Structure
Create the following directory structure:
```
backend/
├── main.py
├── models.py
├── db.py
├── routes/
│   └── tasks.py
├── utils/
│   ├── auth.py
│   └── jwt_handler.py
└── .env
```

## Running the Application

### Development
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Base URL
`http://localhost:8000/api/{user_id}/tasks`

### Available Endpoints
- `GET /api/{user_id}/tasks` - Get all tasks for user
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Update completion status

## Authentication
Include JWT token in Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## Testing the API

### Using curl
```bash
# Get all tasks for user
curl -H "Authorization: Bearer <token>" \
     http://localhost:8000/api/user123/tasks

# Create a new task
curl -X POST \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"title":"New Task","description":"Task description"}' \
     http://localhost:8000/api/user123/tasks
```

## Database Initialization
On first run, the application will automatically create the required tables based on the models.

## Troubleshooting

### Common Issues
1. **Database Connection Error**: Verify DATABASE_URL in .env
2. **JWT Token Error**: Ensure BETTER_AUTH_SECRET matches frontend
3. **Port Already in Use**: Change port in uvicorn command

### Logs
Check console output for detailed error messages during development.