from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import GroupRepository
from app.ddd.service.usecases.group import GroupAddMemberUseCase
from app.schemas.users import GroupUsers, UsersAddRequest

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return GroupAddMemberUseCase(db,GroupRepository(db))



@router.post("/", response_model=GroupUsers)
async def member_add(group_id: str,request:UsersAddRequest, usecase:GroupAddMemberUseCase=Depends(__usecase_di)):
    members=usecase.execute(group_id,request.user_ids)
    response=[member.to_dict() for member in members]
    return {"users":response}
    
