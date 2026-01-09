# Todo API Backend

A FastAPI-based backend for the Todo application with JWT authentication and PostgreSQL database.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials and secret key
```

4. Run the application:
```bash
uvicorn main:app --reload
```

## API Endpoints

The API follows the structure: `/api/{user_id}/tasks`

### Available Endpoints

- `GET /api/{user_id}/tasks` - Get all tasks for user
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Update completion status

## Authentication

All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL database connection string
- `BETTER_AUTH_SECRET`: Secret key for JWT token signing