from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import MemberRepository, UserRepository
from app.ddd.service.usecases.group import GroupGetAllMemberUseCase

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return GroupGetAllMemberUseCase(MemberRepository(db),UserRepository(db))


class MemberResponse(BaseModel):
    id:UUID
    name:str
    room_number:str
    point:float
    is_active:bool
    class Config:
        orm_mode = True

class GroupGetAllMemberResponse(BaseModel):
    users:list[MemberResponse]
    class Config:
        orm_mode = True

@router.get("/", response_model=GroupGetAllMemberResponse)
async def member_getall(group_id: str,
                        room_number:str|None=None, 
                        usecase:GroupGetAllMemberUseCase=Depends(__usecase_di)):
    members=usecase.execute(group_id,room_number)
    return {"users":members}
    
