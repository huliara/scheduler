from database import get_db
from ddd.infra.repository import (GroupRepository, TaskRepository,
                                  TemplateRepository)
from ddd.service.usecases.template import TemplatePostUseCase
from fastapi import APIRouter, Depends
from schemas.template import TemplateCreate, TemplateDisplay
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TemplatePostUseCase(TemplateRepository(db),
                               GroupRepository(db),
                               TaskRepository(db))


@router.post("/", response_model=TemplateDisplay)
async def template_get(request:TemplateCreate, usecase:TemplatePostUseCase=Depends(__usecase_di)):
    response=usecase.execute(request).to_dict()
    return response
    
