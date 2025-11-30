from uuid import UUID

from database import get_db
from ddd.infra.repository import ShiftRepository
from ddd.service.usecases.shift import ShiftRemoveUseCase
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return ShiftRemoveUseCase(ShiftRepository(db))

class TaskDeleteResponse(BaseModel):
    id: UUID
    name: str


@router.delete("/{task_id}", response_model=TaskDeleteResponse)
async def template_get(task_id:str, usecase:ShiftRemoveUseCase=Depends(__usecase_di)):
    response=usecase.execute(task_id)
    return {
        "id": response.id,
        "name": response.name
    }
    
