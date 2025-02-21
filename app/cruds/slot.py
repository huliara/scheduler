import datetime

from fastapi import HTTPException, status
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.cruds.response import slot_display, slots_display
from app.models.models import GroupUser, Task, TaskDetail, User
from app.schemas.slot import SlotCreate


def all(db: Session):
    items = db.scalars(select(Task)).all()

    return slots_display(items)


def slot_finished(db: Session):
    item = (
        db.execute(select(Task).filter(Task.end_time < datetime.datetime.now()))
        .scalars()
        .all()
    )
    return slots_display(item)


def get(name: str, db: Session):
    item = db.scalars(select(Task).filter_by(name=name).limit(1)).first()
    respone_slot = slot_display(item)
    return respone_slot


def post(request: SlotCreate, db: Session, user: User):
    task = db.get(TaskDetail, request.task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    new_slot = Task(
        name=request.name,
        start_time=request.start_time,
        task_id=request.task_id,
        creater_id=user.id,
    )
    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)
    return new_slot


def patch(request: SlotCreate, slot_id: str, db: Session):
    slot = db.get(Task, slot_id)
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No note with this id: {slot_id} found",
        )
    task = db.get(TaskDetail, request.task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    db.execute(
        update(Task)
        .where(Task.id == slot_id)
        .values(
            name=request.name if request.name else slot.name,
        )
        .execution_options(synchronize_session="evaluate")
    )
    slot.start_time = request.start_time
    slot.end_time = request.end_time
    slot.task = task
    db.commit()
    db.refresh(slot)
    return slot


def assign(slot_id: str, user_id: str, db: Session):
    slot = db.get(Task, slot_id)
    user = db.get(User, user_id)
    if not slot or not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if slot.end_time < datetime.datetime.now():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    exp_assignees = list(filter(lambda x: slot.task in x.exp_tasks, slot.workers))
    if len(slot.workers) + 1 > slot.task.max_worker_num:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    if (slot.task not in user.exp_tasks) and slot.task.max_worker_num - len(
        slot.workers
    ) + len(exp_assignees) <= slot.task.exp_worker_num:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    slot.workers.append(user)
    db.commit()
    db.refresh(slot)
    return slot


"""未テスト 動くかわからない"""


def auto_assign(group_id: str, slots: list[Task], db: Session):
    group_user = db.scalars(
        select(GroupUser).filter(GroupUser.group_id == group_id, GroupUser.point < 200)
    ).all()
    group_user_que = [[] for _ in range(250)]
    for user in group_user:
        group_user_que[user.point].append(user)

    target_point = 0
    for slot in slots:
        current_exp_worker = 0
        while current_exp_worker < slot.task.exp_worker_num:
            if target_point >= 200:
                break
            if group_user_que[target_point] == []:
                target_point += 1
                continue
            exp_worker = list(
                filter(
                    lambda user: user.user.has_exp(slot.task),
                    group_user_que[target_point],
                )
            )
            if slot.task.exp_worker_num - current_exp_worker > len(exp_worker):
                slot.workers += exp_worker
                current_exp_worker += len(exp_worker)
                target_point += 1
                group_user_que[target_point] = list(
                    set(group_user_que[target_point]) - set(exp_worker)
                )
                group_user_que[target_point + slot.task.wage] += exp_worker
                continue
            else:
                slot.workers += exp_worker[
                    : slot.task.exp_worker_num - current_exp_worker
                ]
                current_exp_worker += len(
                    exp_worker[: slot.task.exp_worker_num - current_exp_worker]
                )
                group_user_que[target_point] = list(
                    set(group_user_que[target_point])
                    - set(exp_worker[: slot.task.exp_worker_num - current_exp_worker])
                )
                group_user_que[target_point + slot.task.wage] += exp_worker[
                    : slot.task.exp_worker_num - current_exp_worker
                ]
                break

    target_point = 0
    for slot in slots:
        current_worker = 0
        while current_worker < slot.task.max_worker_num - slot.task.exp_worker_num:
            if target_point >= 200:
                break
            if group_user_que[target_point] == []:
                target_point += 1
                continue
            if (
                slot.task.max_worker_num - slot.task.exp_worker_num - current_worker
                > len(group_user_que[target_point])
            ):
                slot.workers += group_user_que[target_point]
                current_worker += len(group_user_que[target_point])
                target_point += 1
                group_user_que[target_point] = []
                group_user_que[target_point + slot.task.wage] += group_user_que[
                    target_point
                ]
                continue
            else:
                slot.workers += group_user_que[target_point][
                    : slot.task.exp_worker_num - current_exp_worker
                ]
                current_worker += len(
                    group_user_que[target_point][
                        : slot.task.max_worker_num
                        - slot.task.exp_worker_num
                        - current_worker
                    ]
                )
                group_user_que[target_point] = group_user_que[target_point][
                    slot.task.max_worker_num
                    - slot.task.exp_worker_num
                    - current_worker :
                ]
                group_user_que[target_point + slot.task.wage] += group_user_que[
                    target_point
                ][
                    : slot.task.max_worker_num
                    - slot.task.exp_worker_num
                    - current_worker
                ]
                break
    db.commit()
    return slots


def complete(group_id, slot_id: str, done: bool, user: User, db: Session):
    slot = db.get(Task, slot_id)
    if slot.start_time > datetime.datetime.now():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    slots = user.tasks
    if slot not in slots:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    group_user = db.scalars(
        select(GroupUser).filter(
            GroupUser.group_id == group_id, GroupUser.user_id == user.id
        )
    ).first()
    if not group_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    slot.workers.remove(user)
    if done:
        group_user.point += slot.task.wage
        if slot.task not in user.exp_tasks:
            user.exp_tasks.append(slot.task)
    db.commit()
    db.refresh(slot)
    return slot


def bulk_delete(group_id: str, slots_id: list[str], db: Session):
    delete_slot = []
    for slot_id in slots_id:
        slot = db.get(Task, slot_id)
        if not slot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"id:{slot_id} is not found",
            )
        if slot.task.group_id != group_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to delete this slot",
            )
        delete_slot.append({"id": slot.id, "name": slot.name})
        db.delete(slot)
    db.commit()
    return delete_slot


def delete_expired_slots(group_id: str, db: Session):
    slots = db.scalars(
        select(Task).join(Task.task).filter(TaskDetail.group_id == group_id)
    ).all()
    expired_slots = []
    for slot in slots:
        if slot.end_time < datetime.datetime.now() and slot.workers == []:
            expired_slots.append({"id": slot.id, "name": slot.name})
            db.delete(slot)
    db.commit()
    return expired_slots
