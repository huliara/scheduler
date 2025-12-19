from uuid import UUID

from fastapi import APIRouter, Depends
from schemas.groups import Member
from sqlalchemy.orm import Session

from database import get_db
from ddd.infra.repository import MemberRepository, UserRepository
from ddd.service.usecases.group import GroupGetAllMemberUseCase

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return GroupGetAllMemberUseCase(MemberRepository(db),UserRepository(db))




@router.get("/", response_model=list[Member])
async def member_getall(group_id: str,
                        room_number:str|None=None, 
                        usecase:GroupGetAllMemberUseCase=Depends(__usecase_di)):
    members=usecase.execute(group_id,room_number)
    return [member.to_dict() for member in members]
    
