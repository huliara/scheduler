from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import ShiftRepository, TaskRepository
from app.ddd.service.usecases.shift import ShiftUpdateUseCase
from app.schemas.task import TaskCreate, TaskDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return ShiftUpdateUseCase(db,ShiftRepository(db),
                             TaskRepository(db))

@router.patch("/{task_id}", response_model=TaskDisplay)
async def task_update(group_id: str,task_id:str,request:TaskCreate, usecase:ShiftUpdateUseCase=Depends(__usecase_di)):
    response=usecase.execute(task_id,request).to_dict()
    return response
    
