from database import get_db
from ddd.infra.repository import ShiftRepository
from ddd.service.usecases.shift import ShiftGetUseCase
from fastapi import APIRouter, Depends
from schemas.shift import ShiftDisplay
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return ShiftGetUseCase(ShiftRepository(db))



@router.get("/{shift_id}", response_model=ShiftDisplay)
async def shift_get(shift_id:str, usecase:ShiftGetUseCase=Depends(__usecase_di)):
    response=usecase.execute(shift_id).to_dict()
    return response
    
