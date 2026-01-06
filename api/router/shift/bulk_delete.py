from database import get_db
from ddd.infra.repository import ShiftRepository
from ddd.service.usecases.shift import ShiftBulkRemoveUseCase
from fastapi import APIRouter, Depends
from schemas.shift import ShiftsDelete, ShiftDisplay
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return ShiftBulkRemoveUseCase(ShiftRepository(db))


@router.delete("/", response_model=ShiftDisplay)
async def shift_bulk_delete(request:ShiftsDelete, 
                            usecase:ShiftBulkRemoveUseCase=Depends(__usecase_di)):
    response=usecase.execute(request.shifts)
    return response
    
