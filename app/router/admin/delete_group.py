from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import GroupRepository
from app.ddd.service.usecases.group import GroupRemoveUseCase

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return GroupRemoveUseCase(db,GroupRepository(db))

@router.delete("/groups/{group_id}")
async def delete_group(group_id:str,usecase:GroupRemoveUseCase=Depends(__usecase_di)):
    user=usecase.execute(group_id).to_dict()
    return user