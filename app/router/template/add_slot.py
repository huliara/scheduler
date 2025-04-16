from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import TaskDetailRepository, TemplateRepository
from app.ddd.service.usecases.template import TemplateAddSlotUseCase
from app.schemas.template import TemplateDisplay, TemplateSlotBase

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TemplateAddSlotUseCase(db,TemplateRepository(db),TaskDetailRepository(db))

@router.patch("/{template_id}/slots", response_model=TemplateDisplay)
async def template_patch_slots(group_id: str,template_id:str,request:TemplateSlotBase, 
                              usecase:TemplateAddSlotUseCase=Depends(__usecase_di)):
    response=usecase.execute(template_id,request).to_dict()
    return response