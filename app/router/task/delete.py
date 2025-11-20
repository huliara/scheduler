from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import TaskRepository
from app.ddd.service.usecases.task import TaskRemoveUseCase
from app.schemas.task import TaskDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TaskRemoveUseCase(TaskRepository(db))


@router.delete("/{detail_id}", response_model=TaskDisplay)
async def task_delete(detail_id:str,
                            usecase:TaskRemoveUseCase=Depends(__usecase_di)):
    response=usecase.execute(detail_id).to_dict()
    return response
    
