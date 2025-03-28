from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import TaskDetailRepository
from app.ddd.service.usecases.taskdetail import TaskDetailGetUseCase
from app.schemas.taskdetail import TaskDetailDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TaskDetailGetUseCase(db,TaskDetailRepository(db))



@router.get("/{taskdetail_id}", response_model=TaskDetailDisplay)
async def taskdetail_get(group_id: str,taskdetail_id:str, usecase:TaskDetailGetUseCase=Depends(__usecase_di)):
    response=usecase.execute(taskdetail_id).to_dict()
    return response
    
