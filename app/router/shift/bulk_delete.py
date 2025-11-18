from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import ShiftRepository
from app.ddd.service.usecases.shift import ShiftBulkRemoveUseCase
from app.schemas.task import TaskDelete, TaskDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return ShiftBulkRemoveUseCase(db,ShiftRepository)


@router.delete("/", response_model=TaskDisplay)
async def task_bulk_delete(group_id: str,expired:bool|None=None,request:TaskDelete|None=None, usecase:ShiftBulkRemoveUseCase=Depends(__usecase_di)):
    response=usecase.execute(group_id,expired,request.tasks)
    return response
    
