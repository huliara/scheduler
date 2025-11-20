from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import ShiftRepository
from app.ddd.service.usecases.shift import ShiftRemoveUseCase

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
    
