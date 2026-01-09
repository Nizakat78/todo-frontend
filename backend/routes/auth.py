from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select
from datetime import timedelta
from typing import Optional
import uuid
from datetime import datetime

from models import User, UserCreate, UserResponse, UserLogin
from db import get_session
from utils.jwt_handler import create_access_token
from utils.auth import get_current_user
from utils.logging import SecurityLogger, get_logger

router = APIRouter(tags=["auth"])

# Initialize logger
logger = get_logger(__name__)

@router.post("/auth/login", response_model=UserResponse)
async def login(
    user_credentials: UserLogin,
    session: Session = Depends(get_session)
):
    """
    Authenticate user and return JWT token
    """
    # Find user by email
    statement = select(User).where(User.email == user_credentials.email)
    user_result = session.exec(statement)
    user = user_result.first()

    if not user or user.password != user_credentials.password:  # In real app, use hashed passwords
        logger.info(f"Failed login attempt for email: {user_credentials.email}")
        SecurityLogger.log_failed_login_attempt(user_credentials.email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token
    access_token_expires = timedelta(minutes=15)  # 15 minutes expiry
    token_data = {"sub": str(user.id)}
    access_token = create_access_token(
        data=token_data, expires_delta=access_token_expires
    )

    logger.info(f"Successful login for user: {user.id}")
    SecurityLogger.log_successful_login(str(user.id))

    return UserResponse(
        success=True,
        data={
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat()
        },
        token=access_token,
        timestamp=datetime.utcnow().isoformat()
    )


@router.post("/auth/signup", response_model=UserResponse)
async def signup(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    """
    Register a new user and return JWT token
    """
    # Check if user already exists
    statement = select(User).where(User.email == user_data.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        logger.info(f"Signup attempt with existing email: {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    # Create new user
    user = User(
        email=user_data.email,
        name=user_data.name,
        password=user_data.password  # In real app, hash the password
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Create JWT token
    access_token_expires = timedelta(minutes=15)  # 15 minutes expiry
    token_data = {"sub": str(user.id)}
    access_token = create_access_token(
        data=token_data, expires_delta=access_token_expires
    )

    logger.info(f"New user registered: {user.id}")
    SecurityLogger.log_user_registration(str(user.id))

    return UserResponse(
        success=True,
        data={
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat()
        },
        token=access_token,
        timestamp=datetime.utcnow().isoformat()
    )


@router.post("/auth/logout")
async def logout(current_user: str = Depends(get_current_user)):
    """
    Logout user (client-side token removal is sufficient)
    """
    logger.info(f"User logged out: {current_user}")
    SecurityLogger.log_logout(current_user)

    return {"message": "Successfully logged out"}


@router.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user_id: str = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Get current authenticated user's information
    """
    # Get user from database
    user = session.get(User, current_user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Create a temporary token for the response (same as the one used for auth)
    access_token_expires = timedelta(minutes=15)
    token_data = {"sub": str(user.id)}
    access_token = create_access_token(
        data=token_data, expires_delta=access_token_expires
    )

    return UserResponse(
        success=True,
        data={
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat()
        },
        token=access_token,
        timestamp=datetime.utcnow().isoformat()
    )