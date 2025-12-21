from database import get_db
from ddd.infra.repository import GroupRepository, MemberRepository
from ddd.service.usecases.group import GroupAddMemberUseCase
from fastapi import APIRouter, Depends
from schemas.users import MemberDisplay, UsersAddRequest
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return GroupAddMemberUseCase(GroupRepository(db),MemberRepository(db))



@router.post("/", response_model=list[MemberDisplay])
async def member_add(group_id: str,request:UsersAddRequest, usecase:GroupAddMemberUseCase=Depends(__usecase_di)):
    members=usecase.execute(group_id,request.user_ids)
    response=[member.to_dict() for member in members]
    return response
    
