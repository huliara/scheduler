from datetime import timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.cruds.auth import (authenticate_user, create_access_token,
                            get_current_active_user)
from app.cruds.response import tasks_display, user_detail_display
from app.database import get_db
from app.models.models import GroupUser, TaskDetail, User
from app.schemas.users import UserUpdate

ACCESS_TOKEN_EXPIRE_MINUTES = 60


router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str
    id: UUID
    name: str


"""
@router.post("/register", response_model=AdminUserDisplay)
async def user_register(user: AdminUserCreate, db: Session = Depends(get_db)):
    generated_user = crud.create_admin(user, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return user_display(generated_user)
"""


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "id": user.id,
        "name": user.name,
    }


@router.get("/me")
async def get_current_user(user: User = Depends(get_current_active_user)):
    return user_detail_display(user)


@router.patch("/me")
async def update_current_user(
    request: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    current_user.name = request.name
    current_user.room_number = request.room_number
    exp_task = []
    for task_id in request.exp_task:
        task = db.get(TaskDetail, task_id)
        exp_task.append(task)
    current_user.exp_tasks = exp_task
    db.commit()
    db.refresh(current_user)
    return user_detail_display(current_user)


@router.get("/tasks")
async def get_user_tasks(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    group_user = db.scalars(
        select(GroupUser).filter(GroupUser.user_id == user.id)
    ).all()
    tasks = []
    for group in group_user:
        tasks += group.group.tasks
    return tasks_display(tasks)
