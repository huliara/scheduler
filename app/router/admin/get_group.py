from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import GroupRepository
from app.ddd.service.usecases.group import GroupGetUseCase

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return GroupGetUseCase(db,GroupRepository(db))

@router.get("/groups/{group_id}")
async def get_group(group_id:str,usecase:GroupGetUseCase=Depends(__usecase_di)):
    group=usecase.execute(group_id).to_dict()
    return group