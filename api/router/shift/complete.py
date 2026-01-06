from database import get_db
from ddd.infra.auth import get_current_active_user
from ddd.infra.repository import (GroupRepository, MemberRepository,
                                  ShiftRepository, UserRepository)
from ddd.service.usecases.shift import ShiftCompleteUseCase
from fastapi import APIRouter, Depends
from schemas.shift import ShiftDisplay,ShiftComplete
from sqlalchemy.orm import Session

router = APIRouter()



def __usecase_di(db:Session=Depends(get_db)):
    return ShiftCompleteUseCase(ShiftRepository(db),
                               UserRepository(db),
                               GroupRepository(db),
                               MemberRepository(db))

@router.post("/{shift_id}/complete", response_model=ShiftDisplay)
async def task_complete(shift_id:str,
                        request:ShiftComplete,
                      user=Depends(get_current_active_user), 
                      usecase:ShiftCompleteUseCase=Depends(__usecase_di)):
    response=usecase.execute(shift_id,user.id,(request.latitude,request.longitude)).to_dict()
    return response
    
