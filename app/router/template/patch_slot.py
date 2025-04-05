from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import TemplateRepository
from app.ddd.service.usecases.template import TemplateUpdateSlotUseCase
from app.schemas.template import TemplateDisplay, TemplatePatchSlot

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TemplateUpdateSlotUseCase(db,TemplateRepository(db))

@router.patch("/{template_id}/slot", response_model=TemplateDisplay)
async def template_patch_slot(group_id: str,template_id:str,request:TemplatePatchSlot, 
                              usecase:TemplateUpdateSlotUseCase=Depends(__usecase_di)):
    response=usecase.execute(template_id,request.src,request.dst).to_dict()
    return response
    
