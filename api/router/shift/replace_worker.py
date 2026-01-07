from database import get_db
from ddd.domain.user.user_entity import UserEntity
from ddd.infra.auth import get_current_active_user
from ddd.infra.repository import (GroupRepository, ShiftRepository,
                                  MemberRepository, UserRepository)
from ddd.service.usecases.shift import ShiftReplaceWorkerUseCase
from fastapi import APIRouter, Depends
from schemas.shift import  ShiftDisplay,ShiftWorkerReplace
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return ShiftReplaceWorkerUseCase(ShiftRepository(db),
                           UserRepository(db),
                           GroupRepository(db),
                           MemberRepository(db))

@router.patch("/{shift_id}/workers", response_model=ShiftDisplay)
async def shift_replace_worker(shift_id:str,request:ShiftWorkerReplace,
                    user:UserEntity=Depends(get_current_active_user),
                    usecase:ShiftReplaceWorkerUseCase=Depends(__usecase_di)):
    response=usecase.execute(shift_id,user.id,request.new_worker_id).to_dict()
    return response
    
