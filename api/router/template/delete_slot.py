from database import get_db
from ddd.infra.repository import TaskRepository, TemplateRepository
from ddd.service.usecases.template import TemplateDeleteSlotUseCase
from fastapi import APIRouter, Depends
from schemas.template import TemplateDisplay, TemplateSlotBase
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TemplateDeleteSlotUseCase(TemplateRepository(db),TaskRepository(db))

@router.delete("/{template_id}/slots", response_model=TemplateDisplay)
async def template_delete_slots(template_id:str,request:TemplateSlotBase, 
                              usecase:TemplateDeleteSlotUseCase=Depends(__usecase_di)):
    response=usecase.execute(template_id,request).to_dict()
    return response
    
