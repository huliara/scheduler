from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import TemplateRepository
from app.ddd.service.usecases.template import TemplateGetUseCase
from app.schemas.template import TemplateDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TemplateGetUseCase(db,TemplateRepository(db))


@router.get("/{template_id}", response_model=TemplateDisplay)
async def template_get(group_id: str,template_id:str, usecase:TemplateGetUseCase=Depends(__usecase_di)):
    response=usecase.execute(template_id).to_dict()
    return response
    
