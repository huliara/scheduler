from database import get_db
from ddd.infra.repository import GroupRepository
from ddd.service.usecases.group import GroupGetAllUseCase
from fastapi import APIRouter, Depends
from schemas.groups import GroupsDisplay
from sqlalchemy.orm import Session

router=APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return GroupGetAllUseCase(GroupRepository(db))

@router.get("/",response_model=GroupsDisplay)
async def group_getall(usecase:GroupGetAllUseCase=Depends(__usecase_di)):
    groups=usecase.execute()
    response=[group.to_dict() for group in groups]
    return {"groups":response}