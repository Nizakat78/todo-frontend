from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Dict, Any

class APIException(HTTPException):
    """Custom API exception with standardized error format"""

    def __init__(self, status_code: int, error_code: str, message: str, details: Dict[str, Any] = None):
        super().__init__(status_code=status_code, detail=message)
        self.error_code = error_code
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.utcnow().isoformat()

def api_exception_handler(request: Request, exc: APIException):
    """Custom exception handler for standardized error responses"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details
            },
            "timestamp": exc.timestamp
        }
    )

# Define common exception handlers
def auth_exception_handler(request: Request, exc: HTTPException):
    """Handler for authentication errors"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "AUTH_ERROR",
                "message": exc.detail if exc.detail else "Authentication failed"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    )

def validation_exception_handler(request: Request, exc: HTTPException):
    """Handler for validation errors"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": exc.detail if exc.detail else "Validation failed"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    )

def not_found_exception_handler(request: Request, exc: HTTPException):
    """Handler for not found errors"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": exc.detail if exc.detail else "Resource not found"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    )

def forbidden_exception_handler(request: Request, exc: HTTPException):
    """Handler for forbidden errors"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "FORBIDDEN",
                "message": exc.detail if exc.detail else "Access forbidden"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    )