from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import TaskRepository
from app.ddd.service.usecases.task import TaskGetUseCase
from app.schemas.slot import SlotDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TaskGetUseCase(db,TaskRepository)



@router.get("/{task_id}", response_model=SlotDisplay)
async def template_get(group_id: str,task_id:str, usecase:TaskGetUseCase=Depends(__usecase_di)):
    response=usecase.execute(task_id).to_dict()
    return response
    
