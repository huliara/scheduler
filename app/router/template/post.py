from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import (GroupRepository, TaskDetailRepository,
                                      TemplateRepository)
from app.ddd.service.usecases.template import TemplatePostUseCase
from app.schemas.template import TemplateCreate, TemplateDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TemplatePostUseCase(db,TemplateRepository(db),
                               GroupRepository(db),
                               TaskDetailRepository(db))


@router.post("/", response_model=TemplateDisplay)
async def template_get(group_id: str,request:TemplateCreate, usecase:TemplatePostUseCase=Depends(__usecase_di)):
    response=usecase.execute(group_id,request).to_dict()
    return response
    
