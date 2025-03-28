from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import GroupRepository
from app.ddd.service.usecases.group import GroupPostUseCase
from app.schemas.admin import GroupPostRequest
from app.schemas.groups import GroupsDisplay

router=APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return GroupPostUseCase(db,GroupRepository(db))

@router.post("/groups",response_model=GroupsDisplay)
async def group_post(request:GroupPostRequest,usecase:GroupPostUseCase=Depends(__usecase_di)):
    group=usecase.execute(request.name).to_dict()
    return group