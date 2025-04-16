from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import TaskRepository
from app.ddd.service.usecases.task import TaskRemoveUseCase

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TaskRemoveUseCase(db,TaskRepository(db))

class TaskDeleteResponse(BaseModel):
    id: UUID
    name: str


@router.delete("/{task_id}", response_model=TaskDeleteResponse)
async def template_get(group_id: str,task_id:str, usecase:TaskRemoveUseCase=Depends(__usecase_di)):
    response=usecase.execute(task_id)
    return {
        "id": response.id,
        "name": response.name
    }
    
