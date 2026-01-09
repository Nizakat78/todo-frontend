from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import tasks
from routes import auth
from db import create_db_and_tables
from utils.exceptions import (
    api_exception_handler,
    auth_exception_handler,
    validation_exception_handler,
    not_found_exception_handler,
    forbidden_exception_handler,
    APIException
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(title="Todo API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose authorization header to frontend
    expose_headers=["Access-Control-Allow-Origin"]
)

# Include the auth and tasks routers
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(tasks.router, prefix="/api/{user_id}", tags=["tasks"])

# Add exception handlers
app.add_exception_handler(StarletteHTTPException, auth_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(APIException, api_exception_handler)

@app.on_event("startup")
def on_startup():
    """Create database tables on startup"""
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)