from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.cruds.auth import get_current_active_user
from app.database import get_db
from app.ddd.domain.task import TaskEntity
from app.ddd.infra.repository import GroupRepository, TaskRepository
from app.ddd.service.usecases.task import TaskUpdateUseCase
from app.schemas.taskdetail import TaskDetailCreate, TaskDetailDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TaskUpdateUseCase(db,TaskRepository(db),GroupRepository(db))


@router.patch("/{task_id}", response_model=TaskDetailDisplay)
async def taskdetail_patch(group_id: str,task_id:str,request:TaskDetailCreate,user=Depends(get_current_active_user), usecase:TaskUpdateUseCase=Depends(__usecase_di)):
    params=request.model_dump()
    params["id"]=task_id
    params["creater_id"]=user.id
    params["group_id"]=group_id
    taskdetail=TaskEntity.from_params(params)
    response=usecase.execute(taskdetail).to_dict()
    return response
    
