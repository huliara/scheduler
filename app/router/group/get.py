from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import GroupRepository
from app.ddd.service.usecases.group import GroupGetUseCase
from app.schemas.groups import GroupDisplay

router=APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return GroupGetUseCase(GroupRepository(db))

@router.get("/{group_id}",response_model=GroupDisplay)
async def group_get(group_id:str,usecase:GroupGetUseCase=Depends(__usecase_di)):
    group=usecase.execute(group_id).to_dict()
    return group