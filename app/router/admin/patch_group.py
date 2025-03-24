from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.domain.group import GroupEntity, GroupId
from app.ddd.infra.repository import GroupRepository
from app.ddd.service.usecases.group import GroupUpdateUseCase
from app.schemas.admin import GroupPostRequest

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return GroupUpdateUseCase(db,GroupRepository(db))

@router.patch("/groups/{group_id}")
async def patch_group(group_id:str,request:GroupPostRequest,usecase:GroupUpdateUseCase=Depends(__usecase_di)):
    group_entity=GroupEntity(id=GroupId(group_id),name=request.name)
    user=usecase.execute(group_entity).to_dict()
    return user