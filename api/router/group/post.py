from database import get_db
from ddd.infra.repository import GroupRepository
from ddd.service.usecases.group import GroupPostUseCase
from fastapi import APIRouter, Depends
from schemas.admin import GroupPostRequest
from schemas.groups import GroupDisplay
from sqlalchemy.orm import Session

router=APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return GroupPostUseCase(GroupRepository(db))

@router.post("/",response_model=GroupDisplay)
async def group_post(request:GroupPostRequest,usecase:GroupPostUseCase=Depends(__usecase_di)):
    group=usecase.execute(request.name).to_dict()
    return group