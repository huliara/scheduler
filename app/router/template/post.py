from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.domain.template import TemplateEntity, TemplateSlot
from app.ddd.infra.repository import TemplateRepository
from app.ddd.service.usecases.template import TemplatePostUseCase
from app.schemas.template import TemplateCreate, TemplateDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TemplatePostUseCase(db,TemplateRepository(db))


@router.post("/", response_model=TemplateDisplay)
async def template_get(group_id: str,request:TemplateCreate, usecase:TemplatePostUseCase=Depends(__usecase_di)):
    template_entity=TemplateEntity.from_params(name=request.name,
                                                 group_id=group_id,
                                                 slots=[TemplateSlot(taskdetail_id=slot.id,
                                                                    date_from_start=slot.date_from_start,
                                                                    start_time=slot.start_time)for slot in request.slots])
    response=usecase.execute(template_entity).to_dict()
    return response
    
