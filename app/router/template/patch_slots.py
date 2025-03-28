from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.domain.template import TemplateEntity, TemplateSlot
from app.ddd.infra.repository import TemplateRepository
from app.ddd.service.usecases.template import TemplateUpdateSlotsUseCase
from app.schemas.template import TemplateCreate, TemplateDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TemplateUpdateSlotsUseCase(db,TemplateRepository(db))

@router.patch("/{template_id}/slots", response_model=TemplateDisplay)
async def template_patch_slots(group_id: str,template_id:str,request:TemplateCreate, 
                              usecase:TemplateUpdateSlotsUseCase=Depends(__usecase_di)):
    template=TemplateEntity(id=template_id,name=request.name,
                            slots=[TemplateSlot(taskdetail_id=slot.id,
                                                date_from_start=slot.date_from_start,
                                                start_time=slot.start_time)for slot in request.slots],
                                                group_id=group_id)
    response=usecase.execute(template).to_dict()
    return response
    
