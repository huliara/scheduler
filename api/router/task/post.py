from database import get_db
from ddd.domain.task import TaskEntity
from ddd.infra.auth import get_current_active_user
from ddd.infra.repository import GroupRepository, TaskRepository
from ddd.service.usecases.task import TaskPostUseCase
from fastapi import APIRouter, Depends
from schemas.task import TaskCreate, TaskDisplay
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TaskPostUseCase(TaskRepository(db),GroupRepository(db))


@router.post("/", response_model=TaskDisplay)
async def taskdetail_post(request:TaskCreate,user=Depends(get_current_active_user), usecase:TaskPostUseCase=Depends(__usecase_di)):
    params=request.model_dump()
    params["creater_id"]=user.id
    params["id"]=None
    params["permissions"]=[]
    taskdetail=TaskEntity.from_params(params)
    response=usecase.execute(taskdetail).to_dict()
    response["creater_name"]=user.name
    return response
    
