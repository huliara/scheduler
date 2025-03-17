from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import TaskDetailRepository, TaskRepository
from app.ddd.service.usecases.task import TaskUpdateUseCase
from app.schemas.task import TaskCreate, TaskDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TaskUpdateUseCase(db,TaskRepository(db),
                             TaskDetailRepository(db))

@router.patch("/{task_id}", response_model=TaskDisplay)
async def task_update(group_id: str,task_id:str,request:TaskCreate, usecase:TaskUpdateUseCase=Depends(__usecase_di)):
    response=usecase.execute(task_id,request).to_dict()
    return response
    
