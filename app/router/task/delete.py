from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import TaskRepository
from app.ddd.service.usecases.task import TaskRemoveUseCase
from app.schemas.task import TaskDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TaskRemoveUseCase(db,TaskRepository)


@router.delete("/{task_id}", response_model=TaskDisplay)
async def template_get(group_id: str,task_id:str, usecase:TaskRemoveUseCase=Depends(__usecase_di)):
    response=usecase.execute(task_id).to_dict()
    return response
    
