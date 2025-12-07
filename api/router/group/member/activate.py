from database import get_db
from ddd.infra.repository import MemberRepository
from ddd.service.usecases.group import (GroupActivateMemberUseCase,
                                        GroupDeactivateMemberUseCase)
from fastapi import APIRouter, Depends
from schemas.users import GroupUsers
from sqlalchemy.orm import Session

router = APIRouter()

def __aca_usecase_di(db:Session=Depends(get_db)):
    return GroupActivateMemberUseCase(MemberRepository(db))

def __deac_usecase_di(db:Session=Depends(get_db)):
    return GroupDeactivateMemberUseCase(MemberRepository(db))

@router.post("/{user_id}/activate", response_model=GroupUsers)
async def member_activate(group_id: str,user_id:str, 
                          activate:bool,
                        ac_usecase:GroupActivateMemberUseCase=Depends(__aca_usecase_di),
                        deac_usecase:GroupDeactivateMemberUseCase=Depends(__deac_usecase_di)):
    if activate:
        member=ac_usecase.execute(group_id,user_id).to_dict()
    else:
        member=deac_usecase.execute(group_id,user_id).to_dict()
    return member
    
