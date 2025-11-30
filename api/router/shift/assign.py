from database import get_db
from ddd.infra.auth import get_current_active_user
from ddd.infra.repository import ShiftRepository, UserRepository
from ddd.service.usecases.shift import ShiftAssignUseCase
from fastapi import APIRouter, Depends
from schemas.shift import ShiftDisplay
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return ShiftAssignUseCase(ShiftRepository(db),UserRepository(db))

@router.post("/{shift_id}/assign", response_model=ShiftDisplay)
async def task_assign(shift_id:str,
                      user=Depends(get_current_active_user), 
                      usecase:ShiftAssignUseCase=Depends(__usecase_di)):
    response=usecase.execute(shift_id,user.id).to_dict()
    return response
    
