from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import GroupRepository, MemberRepository
from app.ddd.service.usecases.group import GroupAddMemberUseCase
from app.schemas.admin import AddUserRequest

router=APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return GroupAddMemberUseCase(db,GroupRepository(db),MemberRepository(db))

@router.post("/groups/{group_id}/members")
async def add_group_member(group_id:str,request:AddUserRequest,usecase:GroupAddMemberUseCase=Depends(__usecase_di)):
    members=usecase.execute(group_id,request.users)
    response=[member.to_dict() for member in members]
    return response