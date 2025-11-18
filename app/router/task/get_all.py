from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import TaskRepository
from app.ddd.service.usecases.task import TaskGetAllUseCase
from app.schemas.taskdetail import TaskDetailList

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TaskGetAllUseCase(db,TaskRepository(db))



@router.get("/", response_model=TaskDetailList)
async def taskdetail_getall(group_id: str, usecase:TaskGetAllUseCase=Depends(__usecase_di)):
    taskdetail=usecase.execute(group_id)
    response=[task.to_dict() for task in taskdetail]
    return {'tasks':response}
    
