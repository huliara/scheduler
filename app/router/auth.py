from datetime import timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.cruds.auth import (authenticate_user, create_access_token,
                            get_current_active_user)
from app.database import get_db
from app.models.models import GroupUser, TaskDetail, User
from app.schemas.users import UserUpdate


def response_base(model):
    return {
        "id": model.id,
        "name": model.name,
    }
    
def user_display(user: User):
    return {
        "id": user.id,
        "name": user.name,
        "room_number": user.room_number,
        "is_active": user.is_active,
    }
    
def user_detail_display(user: User):
    return user_display(user) | {
        "groups": [
            {"id": group.group_id, "name": group.group.name} for group in user.groups
        ],
        "exp_tasks": [response_base(task) for task in user.exp_tasks],
        "slots": [response_base(slot) for slot in user.tasks],
        "create_slot": [response_base(slot) for slot in user.create_tasks],
        "create_task": [response_base(task) for task in user.create_taskdetail],
        "is_admin": user.is_admin,
    }

def task_display(task: TaskDetail):
    return {
        "id": task.id,
        "name": task.name,
        "detail": task.detail,
        "max_worker_num": task.max_worker,
        "min_worker_num": task.min_worker,
        "exp_worker_num": task.exp_worker,
        "point": task.wage,
        "duration": int(task.duration.total_seconds()),
        "creater_id": task.creater_id,
        "creater_name": task.creater.name,
        "group_id": task.group_id,
    }


def tasks_display(tasks: TaskDetail):
    return [task_display(task) for task in tasks]

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
