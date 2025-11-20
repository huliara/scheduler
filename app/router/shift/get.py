from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import ShiftRepository
from app.ddd.service.usecases.shift import ShiftGetUseCase
from app.schemas.shift import ShiftDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return ShiftGetUseCase(ShiftRepository(db))



@router.get("/{shift_id}", response_model=ShiftDisplay)
async def shift_get(shift_id:str, usecase:ShiftGetUseCase=Depends(__usecase_di)):
    response=usecase.execute(shift_id).to_dict()
    return response
    
