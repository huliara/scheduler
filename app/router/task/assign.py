from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.cruds.auth import get_current_active_user
from app.database import get_db
from app.ddd.infra.repository import TaskRepository, UserRepository
from app.ddd.service.usecases.task import TaskAssignUseCase
from app.schemas.task import TaskDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TaskAssignUseCase(db,TaskRepository(db),UserRepository(db))

@router.post("/{task_id}/assign", response_model=TaskDisplay)
async def task_assign(group_id: str,task_id:str,
                      user=Depends(get_current_active_user), 
                      usecase:TaskAssignUseCase=Depends(__usecase_di)):
    response=usecase.execute(task_id,user.id).to_dict()
    return response
    
