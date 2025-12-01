from database import get_db
from ddd.infra.repository import TemplateRepository
from ddd.service.usecases.template import TemplateGetUseCase
from fastapi import APIRouter, Depends
from schemas.template import TemplateDisplay
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TemplateGetUseCase(TemplateRepository(db))


@router.get("/{template_id}", response_model=TemplateDisplay)
async def template_get(template_id:str, usecase:TemplateGetUseCase=Depends(__usecase_di)):
    response=usecase.execute(template_id).to_dict()
    return response
    
