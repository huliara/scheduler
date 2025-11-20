from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import TemplateRepository
from app.ddd.service.usecases.template import TemplateUpdateNameUseCase
from app.schemas.template import TemplateCreateBase, TemplateDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TemplateUpdateNameUseCase(TemplateRepository(db))

@router.patch("/{template_id}", response_model=TemplateDisplay)
async def template_patch_name(template_id:str,request:TemplateCreateBase, usecase:TemplateUpdateNameUseCase=Depends(__usecase_di)):
    response=usecase.execute(template_id,request.name).to_dict()
    return response
    
