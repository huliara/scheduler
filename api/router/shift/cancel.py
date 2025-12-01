from database import get_db
from ddd.infra.auth import get_current_active_user
from ddd.infra.repository import ShiftRepository, UserRepository
from ddd.service.usecases.shift import ShiftCancelUseCase
from fastapi import APIRouter, Depends
from schemas.shift import ShiftDisplay
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return ShiftCancelUseCase(ShiftRepository(db),UserRepository(db))

@router.post("/{shift_id}/cancel", response_model=ShiftDisplay)
async def task_cancel(shift_id:str,
                      user=Depends(get_current_active_user), 
                      usecase:ShiftCancelUseCase=Depends(__usecase_di)):
    response=usecase.execute(shift_id,user.id).to_dict()
    return response
    
