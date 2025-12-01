from database import get_db
from ddd.infra.repository import TemplateRepository
from ddd.service.usecases.template import TemplateGetAllUseCase
from fastapi import APIRouter, Depends
from schemas.template import TemplateList
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TemplateGetAllUseCase(TemplateRepository(db))


@router.get("/", response_model=TemplateList)
async def template_getall(group_id:str|None=None,usecase:TemplateGetAllUseCase=Depends(__usecase_di)):
    template_entities=usecase.execute(group_id)
    response=[template.to_dict() for template in template_entities]
    return {"templates":response}
    
