from fastapi import HTTPException, status
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session, joinedload

from app.cruds.response import task_display, tasks_display
from app.models.models import TaskDetail, User
from app.schemas.task import TaskCreate


def all(db: Session):
    items = db.scalars(select(TaskDetail).options(joinedload(TaskDetail.creater))).unique().all()
    return tasks_display(items)


async def task_get(name: str, db: Session):
    item = db.scalars(select(TaskDetail).filter_by(name=name).limit(1)).first()
    return item


def post(task: TaskCreate, current_user: User, db: Session):
    task = TaskDetail(creater=current_user, **task.dict())
    db.add(task)
    db.commit()
    return task_display(task)


def delete(name: str, db: Session):
    db.scalars(select(TaskDetail).filter_by(name=name)).delete()
    db.commit()
    return name


def patch(request: TaskCreate, task_id: str, db: Session):
    task = db.get(TaskDetail, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No note with this id: {task_id} found",
        )

    db.execute(
        update(TaskDetail)
        .where(TaskDetail.id == task_id)
        .values(
            name=request.name if request.name else task.name,
            detail=request.detail if request.detail else task.detail,
            max_worker_num=request.max_worker_num
            if request.max_worker_num
            else task.max_worker,
            min_worker_num=request.min_worker_num
            if request.min_worker_num
            else task.min_worker,
            exp_worker_num=request.exp_worker_num
            if request.exp_worker_num
            else task.exp_worker,
            point=request.point if request.point else task.wage,
            duration=request.duration if request.duration else task.duration,
        )
        .execution_options(synchronize_session="evaluate")
    )
    db.commit()
    return task
