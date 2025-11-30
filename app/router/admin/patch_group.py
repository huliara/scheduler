from database import get_db
from ddd.domain.group import GroupEntity, GroupId
from ddd.infra.repository import GroupRepository
from ddd.service.usecases.group import GroupUpdateUseCase
from fastapi import APIRouter, Depends
from schemas.admin import GroupPostRequest
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return GroupUpdateUseCase(db,GroupRepository(db))

@router.patch("/groups/{group_id}")
async def patch_group(group_id:str,request:GroupPostRequest,usecase:GroupUpdateUseCase=Depends(__usecase_di)):
    group_entity=GroupEntity(id=GroupId(group_id),name=request.name)
    user=usecase.execute(group_entity).to_dict()
    return user