from database import get_db
from ddd.infra.auth import get_current_active_user
from ddd.infra.repository import GroupRepository, MemberRepository
from ddd.service.usecases.group import GroupAddMemberUseCase
from fastapi import APIRouter, Depends
from schemas.users import MemberDisplay
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return GroupAddMemberUseCase(GroupRepository(db),MemberRepository(db))



@router.post("/join", response_model=list[MemberDisplay])
async def member_join(group_id: str,
                      user=Depends(get_current_active_user), 
                      usecase:GroupAddMemberUseCase=Depends(__usecase_di)):
    members=usecase.execute(group_id,[user.id])
    response=[member.to_dict() for member in members]
    return response
    
