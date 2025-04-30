from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.cruds.auth import get_current_active_user
from app.database import get_db
from app.ddd.infra.repository import (GroupRepository, MemberRepository,
                                      TaskRepository, UserRepository)
from app.ddd.service.usecases.task import TaskCompleteUseCase
from app.schemas.task import TaskDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TaskCompleteUseCase(db,TaskRepository(db),
                               UserRepository(db),
                               GroupRepository(db),
                               MemberRepository(db))

@router.post("/{task_id}/complete", response_model=TaskDisplay)
async def task_complete(group_id: str,task_id:str,
                      user=Depends(get_current_active_user), 
                      usecase:TaskCompleteUseCase=Depends(__usecase_di)):
    response=usecase.execute(group_id,task_id,user.id).to_dict()
    return response
    
