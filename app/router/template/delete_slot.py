from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import TaskRepository, TemplateRepository
from app.ddd.service.usecases.template import TemplateDeleteSlotUseCase
from app.schemas.template import TemplateDisplay, TemplateSlotBase

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TemplateDeleteSlotUseCase(db,TemplateRepository(db),TaskRepository(db))

@router.delete("/{template_id}/slots", response_model=TemplateDisplay)
async def template_delete_slots(group_id: str,template_id:str,request:TemplateSlotBase, 
                              usecase:TemplateDeleteSlotUseCase=Depends(__usecase_di)):
    response=usecase.execute(template_id,request).to_dict()
    return response
    
