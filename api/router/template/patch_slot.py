from database import get_db
from ddd.infra.repository import TemplateRepository
from ddd.service.usecases.template import TemplateUpdateSlotUseCase
from fastapi import APIRouter, Depends
from schemas.template import TemplateDisplay, TemplatePatchSlot
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TemplateUpdateSlotUseCase(TemplateRepository(db))

@router.patch("/{template_id}/slot", response_model=TemplateDisplay)
async def template_patch_slot(template_id:str,request:TemplatePatchSlot, 
                              usecase:TemplateUpdateSlotUseCase=Depends(__usecase_di)):
    response=usecase.execute(template_id,request.src,request.dst).to_dict()
    return response
    
