from database import get_db
from ddd.infra.repository import TaskRepository
from ddd.service.usecases.task import TaskGetUseCase
from fastapi import APIRouter, Depends
from schemas.task import TaskDisplay
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TaskGetUseCase(TaskRepository(db))



@router.get("/{task_id}", response_model=TaskDisplay)
async def taskdetail_get(task_id:str, usecase:TaskGetUseCase=Depends(__usecase_di)):
    response=usecase.execute(task_id).to_dict()
    return response
    
