import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.orm import Session

import app.cruds.slot as crud
from app.cruds.auth import check_privilege, get_current_active_user
from app.cruds.response import slot_display
from app.database import get_db
from app.models.models import Task, TaskDetail, User
from app.schemas.task import (TaskComplete, TaskCreate, TaskDelete,
                              TaskDisplay, TaskList)

router = APIRouter()


@router.post("/{slot_id}/complete")
async def slot_complete(
    group_id: str,
    slot_id: str,
    request: TaskComplete,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    check_privilege(group_id, user.id, "normal", db)
    slot = crud.complete(group_id, slot_id, request.done, user, db)
    return slot_display(slot)
