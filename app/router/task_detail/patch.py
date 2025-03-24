from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.cruds.auth import get_current_active_user
from app.database import get_db
from app.ddd.domain.task_detail import TaskDetailEntity
from app.ddd.infra.repository import GroupRepository, TaskDetailRepository
from app.ddd.service.usecases.taskdetail import TaskDetailUpdateUseCase
from app.schemas.taskdetail import TaskDetailCreate, TaskDetailDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TaskDetailUpdateUseCase(db,TaskDetailRepository(db),GroupRepository(db))


@router.patch("/{task_id}", response_model=TaskDetailDisplay)
async def taskdetail_patch(group_id: str,task_id:str,request:TaskDetailCreate,user=Depends(get_current_active_user), usecase:TaskDetailUpdateUseCase=Depends(__usecase_di)):
    params=request.model_dump()
    params["id"]=task_id
    params["creater_id"]=user.id
    params["group_id"]=group_id
    taskdetail=TaskDetailEntity.from_params(params)
    response=usecase.execute(taskdetail).to_dict()
    return response
    
