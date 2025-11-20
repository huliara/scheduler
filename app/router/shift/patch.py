from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import ShiftRepository, TaskRepository
from app.ddd.service.usecases.shift import ShiftUpdateUseCase
from app.schemas.shift import ShiftCreate, ShiftDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return ShiftUpdateUseCase(ShiftRepository(db),
                             TaskRepository(db))

@router.patch("/{shift_id}", response_model=ShiftDisplay)
async def shift_update(shift_id:str,request:ShiftCreate, usecase:ShiftUpdateUseCase=Depends(__usecase_di)):
    response=usecase.execute(shift_id,request).to_dict()
    return response
    
