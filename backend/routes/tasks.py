from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime
import uuid

from models import Task, TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from db import get_session
from utils.auth import get_current_user
from utils.logging import SecurityLogger, get_logger

router = APIRouter(tags=["tasks"])

# Initialize logger
logger = get_logger(__name__)

@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user:
        logger.warning(f"Unauthorized attempt to create task for user {user_id} by user {current_user}")
        SecurityLogger.log_unauthorized_access(current_user, f"create_task_for_user_{user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    # Create the task
    task = Task(
        title=task_data.title,
        description=task_data.description,
        completed=False,
        user_id=user_id
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    logger.info(f"Task created successfully for user {user_id}, task_id: {task.id}")
    return TaskResponse(success=True, data=task, timestamp=datetime.utcnow().isoformat())


@router.get("/tasks", response_model=TaskListResponse)
async def get_tasks(
    user_id: str,
    completed: Optional[bool] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user:
        logger.warning(f"Unauthorized attempt to view tasks for user {user_id} by user {current_user}")
        SecurityLogger.log_unauthorized_access(current_user, f"view_tasks_for_user_{user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view tasks for this user"
        )

    # Build the query
    query = select(Task).where(Task.user_id == user_id)

    if completed is not None:
        query = query.where(Task.completed == completed)

    # Get total count for pagination metadata
    total_query = select(Task).where(Task.user_id == user_id)
    if completed is not None:
        total_query = total_query.where(Task.completed == completed)

    total_count = len(session.exec(total_query).all())

    # Apply pagination
    query = query.offset(offset).limit(limit)
    tasks = session.exec(query).all()

    logger.info(f"Retrieved {len(tasks)} tasks for user {user_id} with filter completed={completed}")
    return TaskListResponse(
        success=True,
        data=tasks,
        meta={"total": total_count, "limit": limit, "offset": offset},
        timestamp=datetime.utcnow().isoformat()
    )


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user:
        logger.warning(f"Unauthorized attempt to view task {task_id} for user {user_id} by user {current_user}")
        SecurityLogger.log_unauthorized_access(current_user, f"view_task_{task_id}_for_user_{user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view tasks for this user"
        )

    # Get the specific task
    task = session.get(Task, task_id)

    if not task:
        logger.info(f"Task {task_id} not found for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != user_id:
        logger.warning(f"User {current_user} attempted to access task {task_id} belonging to user {task.user_id}")
        SecurityLogger.log_unauthorized_access(current_user, f"access_task_{task_id}_belonging_to_user_{task.user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    logger.info(f"Task {task_id} retrieved successfully for user {user_id}")
    return TaskResponse(success=True, data=task, timestamp=datetime.utcnow().isoformat())


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user:
        logger.warning(f"Unauthorized attempt to update task {task_id} for user {user_id} by user {current_user}")
        SecurityLogger.log_unauthorized_access(current_user, f"update_task_{task_id}_for_user_{user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update tasks for this user"
        )

    # Get the task to update
    task = session.get(Task, task_id)

    if not task:
        logger.info(f"Task {task_id} not found for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != user_id:
        logger.warning(f"User {current_user} attempted to update task {task_id} belonging to user {task.user_id}")
        SecurityLogger.log_unauthorized_access(current_user, f"update_task_{task_id}_belonging_to_user_{task.user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Update the task
    task.title = task_data.title
    task.description = task_data.description
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    logger.info(f"Task {task_id} updated successfully for user {user_id}")
    return TaskResponse(success=True, data=task, timestamp=datetime.utcnow().isoformat())


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str,
    task_id: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user:
        logger.warning(f"Unauthorized attempt to delete task {task_id} for user {user_id} by user {current_user}")
        SecurityLogger.log_unauthorized_access(current_user, f"delete_task_{task_id}_for_user_{user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete tasks for this user"
        )

    # Get the task to delete
    task = session.get(Task, task_id)

    if not task:
        logger.info(f"Task {task_id} not found for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != user_id:
        logger.warning(f"User {current_user} attempted to delete task {task_id} belonging to user {task.user_id}")
        SecurityLogger.log_unauthorized_access(current_user, f"delete_task_{task_id}_belonging_to_user_{task.user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    session.delete(task)
    session.commit()

    logger.info(f"Task {task_id} deleted successfully for user {user_id}")
    return


@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
async def update_task_completion(
    user_id: str,
    task_id: int,
    completed_data: dict,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user:
        logger.warning(f"Unauthorized attempt to update completion status for task {task_id} for user {user_id} by user {current_user}")
        SecurityLogger.log_unauthorized_access(current_user, f"update_completion_task_{task_id}_for_user_{user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update tasks for this user"
        )

    # Validate the completed data
    if "completed" not in completed_data or not isinstance(completed_data["completed"], bool):
        logger.info(f"Invalid completion data received for task {task_id}: {completed_data}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request body: 'completed' field must be a boolean"
        )

    # Get the task to update
    task = session.get(Task, task_id)

    if not task:
        logger.info(f"Task {task_id} not found for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != user_id:
        logger.warning(f"User {current_user} attempted to update completion status for task {task_id} belonging to user {task.user_id}")
        SecurityLogger.log_unauthorized_access(current_user, f"update_completion_task_{task_id}_belonging_to_user_{task.user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Update the completion status
    task.completed = completed_data["completed"]
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    logger.info(f"Task {task_id} completion status updated to {task.completed} for user {user_id}")
    return TaskResponse(success=True, data=task, timestamp=datetime.utcnow().isoformat())