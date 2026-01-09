from sqlmodel import create_engine, Session
from models import Task
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

# Create the engine with SQLite thread-safe settings
if DATABASE_URL.startswith("sqlite"):
    # Use SQLite with thread-safe settings for web applications
    engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """Create database tables"""
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)