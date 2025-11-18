from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import TaskRepository
from app.ddd.service.usecases.task import TaskGetUseCase
from app.schemas.taskdetail import TaskDetailDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TaskGetUseCase(db,TaskRepository(db))



@router.get("/{taskdetail_id}", response_model=TaskDetailDisplay)
async def taskdetail_get(group_id: str,taskdetail_id:str, usecase:TaskGetUseCase=Depends(__usecase_di)):
    response=usecase.execute(taskdetail_id).to_dict()
    return response
    
