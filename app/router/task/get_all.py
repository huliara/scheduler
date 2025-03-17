from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import TaskRepository
from app.ddd.service.usecases.task import TaskGetAllUseCase
from app.schemas.task import TaskList

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TaskGetAllUseCase(db,TaskRepository)



@router.get("/", response_model=TaskList)
async def task_getall(group_id: str,end:bool|None=None,usecase:TaskGetAllUseCase=Depends(__usecase_di)):
    tasks=usecase.execute(group_id,end)
    response=[task.to_dict() for task in tasks]
    return {"tasks":response}
    
