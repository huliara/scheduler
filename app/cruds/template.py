from datetime import date, datetime, time, timedelta

from sqlalchemy.orm import Session

from app.models.models import Task, TaskTemplate, Template, User
from app.schemas.template import TemplateCreate


def post(group_id:str,template: TemplateCreate, db: Session):
    db_template = Template(
        name=template.name,
        group_id=group_id,
    )
    for req_task in template.tasks:
        db_task = TaskTemplate(
            task_id=req_task.id,
            date_from_start=req_task.date_from_start,
            start_time=time(
                hour=req_task.start_time.hour,
                minute=req_task.start_time.minute,
            ),
        )
        db_template.tasktemplates.append(db_task) 
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template



def generate_slots(
    template: Template, start_day: date, user: User, db: Session
):
    tasks = template.tasktemplates
    slots = []
    for task in tasks:
        date = start_day+timedelta(days=task.date_from_start)
        start = datetime.combine(date, task.start_time)
        name = (
            str(start.hour)
            + "時"
            + str(start.minute)
            + "分から"
            + str(task.task.name)
        )
        slot = Task(
            creater_id=user.id,
            name=name,
            task_id=task.task_id,
            start_time=start,
        )
        slots.append(slot)
    db.bulk_save_objects(slots)
    db.commit()
    return slots
