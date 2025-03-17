from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.cruds.auth import get_current_active_user
from app.database import get_db
from app.ddd.infra.repository import TaskRepository
from app.ddd.service.usecases.task import TaskCancelUseCase
from app.schemas.task import TaskDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TaskCancelUseCase(db,TaskRepository(db))

@router.post("/{task_id}/cancel", response_model=TaskDisplay)
async def task_cancel(group_id: str,task_id:str,
                      user=Depends(get_current_active_user), 
                      usecase:TaskCancelUseCase=Depends(__usecase_di)):
    response=usecase.execute(task_id,user.id).to_dict()
    return response
    
