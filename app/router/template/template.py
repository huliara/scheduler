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
