from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.cruds.auth import get_current_active_user
from app.database import get_db
from app.ddd.infra.repository import ShiftRepository, UserRepository
from app.ddd.service.usecases.shift import ShiftAssignUseCase
from app.schemas.task import TaskDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return ShiftAssignUseCase(db,ShiftRepository(db),UserRepository(db))

@router.post("/{task_id}/assign", response_model=TaskDisplay)
async def task_assign(group_id: str,task_id:str,
                      user=Depends(get_current_active_user), 
                      usecase:ShiftAssignUseCase=Depends(__usecase_di)):
    response=usecase.execute(task_id,user.id).to_dict()
    return response
    
