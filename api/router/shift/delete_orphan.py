from uuid import UUID

from database import get_db
from ddd.infra.repository import ShiftRepository
from ddd.service.usecases.shift import ShiftRemoveOrphanUseCase
from fastapi import APIRouter, Depends
from schemas.shift import ShiftDisplay
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return ShiftRemoveOrphanUseCase(ShiftRepository(db))

@router.delete("/orphan/{group_id}", response_model=list[ShiftDisplay])
async def template_get(group_id:str, usecase:ShiftRemoveOrphanUseCase=Depends(__usecase_di)):
    response=usecase.execute(group_id)
    return [shift.to_dict() for shift in response]
