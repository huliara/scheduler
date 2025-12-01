from database import get_db
from ddd.infra.repository import ShiftRepository, TaskRepository
from ddd.service.usecases.shift import ShiftUpdateUseCase
from fastapi import APIRouter, Depends
from schemas.shift import ShiftCreate, ShiftDisplay
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return ShiftUpdateUseCase(ShiftRepository(db),
                             TaskRepository(db))

@router.patch("/{shift_id}", response_model=ShiftDisplay)
async def shift_update(shift_id:str,request:ShiftCreate, usecase:ShiftUpdateUseCase=Depends(__usecase_di)):
    response=usecase.execute(shift_id,request).to_dict()
    return response
    
