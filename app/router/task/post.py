from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.ddd.infra.auth import get_current_active_user
from app.database import get_db
from app.ddd.domain.task import TaskEntity
from app.ddd.infra.repository import GroupRepository, TaskRepository
from app.ddd.service.usecases.task import TaskPostUseCase
from app.schemas.task import TaskCreate, TaskDisplay

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
    
