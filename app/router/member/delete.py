from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import GroupRepository, MemberRepository
from app.ddd.service.usecases.group import GroupRemoveMemberUseCase
from app.schemas.users import GroupUsers

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return GroupRemoveMemberUseCase(db,GroupRepository(db),MemberRepository(db))


@router.delete("/{user_id}", response_model=GroupUsers)
async def member_remove(group_id: str,user_id:str, usecase:GroupRemoveMemberUseCase=Depends(__usecase_di)):
    member=usecase.execute(group_id,user_id).to_dict()
    return member
    
