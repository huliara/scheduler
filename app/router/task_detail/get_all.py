from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import TaskDetailRepository
from app.ddd.service.usecases.taskdetail import TaskDetailGetAllUseCase
from app.schemas.taskdetail import TaskDetailList

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TaskDetailGetAllUseCase(db,TaskDetailRepository(db))



@router.get("/", response_model=TaskDetailList)
async def taskdetail_getall(group_id: str, usecase:TaskDetailGetAllUseCase=Depends(__usecase_di)):
    taskdetail=usecase.execute(group_id)
    response=[task.to_dict() for task in taskdetail]
    return response
    
