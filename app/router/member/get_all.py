from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import MemberRepository
from app.ddd.service.usecases.group import GroupGetAllMemberUseCase
from app.schemas.users import GroupUsers

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return GroupGetAllMemberUseCase(db,MemberRepository(db))



@router.get("/", response_model=GroupUsers)
async def member_getall(group_id: str,room_number:str|None=None, usecase:GroupGetAllMemberUseCase=Depends(__usecase_di)):
    members=usecase.execute(group_id,room_number)
    response=[member.to_dict() for member in members]
    return {"users":response}
    
