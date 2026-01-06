from database import get_db
from ddd.domain.task.task_entity import TaskEntity
from ddd.infra.auth import get_current_active_user
from ddd.infra.repository import GroupRepository, TaskRepository
from ddd.service.usecases.task import TaskUpdateUseCase
from fastapi import APIRouter, Depends
from schemas.task import TaskCreate, TaskDisplay
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TaskUpdateUseCase(TaskRepository(db),GroupRepository(db))


@router.patch("/{task_id}", response_model=TaskDisplay)
async def taskdetail_patch(task_id:str,request:TaskCreate,user=Depends(get_current_active_user), 
                           usecase:TaskUpdateUseCase=Depends(__usecase_di)):
    params=request.model_dump()
    params["id"]=task_id
    params["creater_id"]=user.id
    taskdetail=TaskEntity.from_params(params)
    response=usecase.execute(taskdetail).to_dict()
    return response
    
