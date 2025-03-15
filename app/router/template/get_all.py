from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import TemplateRepository
from app.ddd.service.usecases.template import TemplateGetAllUseCase
from app.schemas.template import TemplateList

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TemplateGetAllUseCase(db,TemplateRepository(db))


@router.get("/", response_model=TemplateList)
async def template_getall(group_id: str, usecase:TemplateGetAllUseCase=Depends(__usecase_di)):
    template_entities=usecase.execute(group_id)
    response=[template.to_dict() for template in template_entities]
    return {"templates":response}
    
