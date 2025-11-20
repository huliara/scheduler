from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import GroupRepository
from app.ddd.service.usecases.group import GroupGetAllUseCase
from app.schemas.groups import GroupsDisplay

router=APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return GroupGetAllUseCase(GroupRepository(db))

@router.get("/",response_model=GroupsDisplay)
async def group_getall(usecase:GroupGetAllUseCase=Depends(__usecase_di)):
    groups=usecase.execute()
    response=[group.to_dict() for group in groups]
    return {"groups":response}