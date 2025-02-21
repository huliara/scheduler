import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.cruds import template as crud
from app.cruds.auth import check_privilege, get_current_active_user
from app.cruds.response import tasktemplate_display, template_display
from app.database import get_db
from app.models.models import TaskDetail, TaskTemplate, Template, User
from app.schemas.template import (SlotByTemplate, TemplateCreate,
                                  TemplateCreateBase, TemplateDisplay,
                                  TemplateList, TemplateTaskBase)

router = APIRouter()


@router.get("/", response_model=TemplateList)
async def template_get(group_id: str, db: Session = Depends(get_db)):
    templates = db.scalars(select(Template).filter(Template.group_id == group_id))
    return {"templates": [template_display(template) for template in templates]}


@router.post("/", response_model=TemplateDisplay)
async def template_post(
    group_id: str,
    request: TemplateCreate,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    check_privilege(group_id, user.id, "edit_template", db)
    template = crud.post(group_id, request, db)
    return template_display(template)


@router.get("/{template_id}", response_model=TemplateDisplay)
async def template_get_one(template_id: str, db: Session = Depends(get_db)):
    template = db.get(Template, template_id)
    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return template_display(template)


@router.delete("/{template_id}")
async def template_delete(
    group_id: str,
    template_id: str,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    check_privilege(group_id, user.id, "edit_template", db)
    template = db.get(Template, template_id)
    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(template)
    db.commit()
    return {"id": template.id, "name": template.name}


@router.patch("/{template_id}")
async def template_patch(
    group_id: str,
    template_id: str,
    request: TemplateCreateBase,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    check_privilege(group_id, user.id, "edit_template", db)
    template = db.get(Template, template_id)
    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    template.name = request.name
    db.commit()
    db.refresh(template)
    return template_display(template)


@router.post("/{template_id}/generate")
async def generate_slots_from_template(
    group_id: str,
    template_id: str,
    request: SlotByTemplate,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    check_privilege(group_id, user.id, "add_slot_from_template", db)
    template = db.get(Template, template_id)
    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    start_day = datetime.date(
        request.start_day.year, request.start_day.month, request.start_day.day
    )
    response = crud.generate_slots(template, start_day, user, db)
    return response


@router.post("/{template_id}/tasks")
async def tasktemplate_add(
    group_id: str,
    template_id: str,
    request: TemplateTaskBase,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    check_privilege(group_id, user.id, "edit_template", db)
    template = db.get(Template, template_id)
    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    task = db.get(TaskDetail, request.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    tasktemplate = TaskTemplate(
        task_id=request.id,
        date_from_start=request.date_from_start,
        start_time=datetime.time(
            hour=request.start_time.hour, minute=request.start_time.minute
        ),
    )
    db.add(tasktemplate)
    template.tasktemplates.append(tasktemplate)
    db.commit()
    db.refresh(template)
    return template_display(template)


@router.delete("/{template_id}/tasks/{tasktemplate_id}")
async def tasktemplate_delete(
    group_id: str,
    template_id: str,
    tasktemplate_id: str,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    check_privilege(group_id, user.id, "edit_template", db)
    template = db.get(Template, template_id)
    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    tasktemplate = db.get(TaskTemplate, tasktemplate_id)
    if not tasktemplate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(tasktemplate)
    db.commit()
    db.refresh(template)
    return template_display(template)


@router.patch("/{template_id}/tasks/{tasktemplate_id}")
async def tasktemplate_edit(
    group_id: str,
    template_id: str,
    tasktemplate_id: str,
    request: TemplateTaskBase,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    check_privilege(group_id, user.id, "edit_template", db)
    tasktemplate = db.get(TaskTemplate, tasktemplate_id)
    if not tasktemplate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    task = db.get(TaskDetail, request.id)
    tasktemplate.task_id = request.id if task else tasktemplate.task_id
    tasktemplate.date_from_start = request.date_from_start
    tasktemplate.start_time = datetime.time(
        hour=request.start_time.hour, minute=request.start_time.minute
    )

    db.commit()
    return tasktemplate_display(tasktemplate)
