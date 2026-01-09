"""
Validation script to ensure all modules can be imported correctly
"""

def validate_imports():
    """Validate that all modules can be imported without errors"""
    try:
        print("Validating imports...")

        # Test main application imports
        from main import app
        print("✓ Main application imported successfully")

        # Test models
        from models import Task, TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
        print("✓ Models imported successfully")

        # Test database
        from db import get_session, create_db_and_tables, engine
        print("✓ Database module imported successfully")

        # Test routes
        from routes import tasks
        print("✓ Routes module imported successfully")

        # Test utilities
        from utils.auth import get_current_user, security
        print("✓ Auth utilities imported successfully")

        from utils.jwt_handler import create_access_token, verify_token
        print("✓ JWT handler imported successfully")

        from utils.exceptions import APIException
        print("✓ Exception handler imported successfully")

        from utils.logging import SecurityLogger, get_logger
        print("✓ Logging utilities imported successfully")

        print("\n✓ All modules imported successfully!")
        print("The backend is set up correctly and ready for use.")

        return True

    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    validate_imports()