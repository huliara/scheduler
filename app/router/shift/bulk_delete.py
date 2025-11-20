from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import ShiftRepository
from app.ddd.service.usecases.shift import ShiftBulkRemoveUseCase
from app.schemas.shift import ShiftDelete, ShiftDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return ShiftBulkRemoveUseCase(ShiftRepository)


@router.delete("/", response_model=ShiftDisplay)
async def shift_bulk_delete(expired:bool|None=None,request:ShiftDelete|None=None, usecase:ShiftBulkRemoveUseCase=Depends(__usecase_di)):
    response=usecase.execute(request.group_id,expired,request.shifts)
    return response
    
