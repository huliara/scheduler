from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import TemplateRepository
from app.ddd.service.usecases.template import TemplateRemoveUseCase
from app.schemas.template import TemplateDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TemplateRemoveUseCase(db,TemplateRepository(db))



@router.delete("/{template_id}", response_model=TemplateDisplay)
async def template_delete(group_id:str,template_id:str,usecase:TemplateRemoveUseCase=Depends(__usecase_di)):
    response=usecase.execute(template_id).to_dict()
    return response
    
