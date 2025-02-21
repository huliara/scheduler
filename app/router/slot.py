import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.orm import Session

import app.cruds.slot as crud
from app.cruds.auth import check_privilege, get_current_active_user
from app.cruds.response import slot_display
from app.database import get_db
from app.models.models import Task, TaskDetail, User
from app.schemas.slot import (SlotComplete, SlotCreate, SlotDelete,
                              SlotDisplay, SlotList)

router = APIRouter()


@router.get("/", response_model=SlotList)
async def slot_list(
    group_id: str,
    end: bool | None = None,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    check_privilege(group_id, user.id, "normal", db)
    if end:
        slots = db.scalars(
            select(Task)
            .filter(Task.end_time < datetime.datetime.now())
            .join(Task.task)
            .filter(TaskDetail.group_id == group_id)
        ).all()
        return {"slots": [slot_display(slot) for slot in slots]}
    slots = db.scalars(
        select(Task).join(Task.task).filter(TaskDetail.group_id == group_id)
    ).all()
    return {"slots": [slot_display(slot) for slot in slots]}


@router.post("/", response_model=SlotDisplay)
async def slot_post(
    group_id: str,
    request: SlotCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    check_privilege(group_id, user.id, "edit_slot", db)
    slot = crud.post(request, db, user)
    return slot_display(slot)


@router.delete("/")
async def slots_delete(
    group_id: str,
    expired: bool | None = None,
    request: SlotDelete | None = None,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    check_privilege(group_id, user.id, "edit_slot", db)
    if expired:
        expired_slots = crud.delete_expired_slots(group_id, db)
        return expired_slots
    slots = crud.bulk_delete(group_id, request.slots, db)
    return slots


@router.get("/{slot_id}", response_model=SlotDisplay)
async def slot_get(
    group_id: str,
    slot_id: str,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    check_privilege(group_id, user.id, "normal", db)
    slot = db.get(Task, slot_id)
    if not slot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return slot_display(slot)


@router.patch("/{slot_id}")
async def slot_patch(
    group_id: str,
    slot_id: str,
    request: SlotCreate,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    check_privilege(group_id, user.id, "edit_slot", db)
    slot = crud.patch(request, slot_id, db)
    return slot_display(slot)


@router.delete("/{slot_id}")
async def slot_delete(
    group_id: str,
    slot_id: str,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    check_privilege(group_id, user.id, "edit_slot", db)
    slot = db.get(Task, slot_id)
    if not slot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(slot)
    db.commit()
    return {"id": slot.id, "name": slot.name}


@router.post("/{slot_id}/cancel", response_model=SlotDisplay)
async def slot_cancel(
    group_id: str,
    slot_id: str,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    slot = db.get(Task, slot_id)
    if not slot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if slot.end_time < datetime.datetime.now():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="すでに終了した仕事です。"
        )
    slot.workers.remove(user)
    db.commit()
    db.refresh(slot)
    return slot_display(slot)


@router.post("/{slot_id}/assign", response_model=SlotDisplay)
async def slot_assign(
    group_id: str,
    slot_id: str,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    check_privilege(group_id, user.id, "normal", db)
    slot = crud.assign(slot_id, user.id, db)
    return slot_display(slot)


@router.post("/{slot_id}/complete")
async def slot_complete(
    group_id: str,
    slot_id: str,
    request: SlotComplete,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    check_privilege(group_id, user.id, "normal", db)
    slot = crud.complete(group_id, slot_id, request.done, user, db)
    return slot_display(slot)
