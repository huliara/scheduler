from database import get_db
from ddd.domain.user.user_entity import UserEntity
from ddd.infra.auth import get_current_active_user
from ddd.infra.repository import (GroupRepository, ShiftRepository,
                                  TaskRepository, UserRepository)
from ddd.service.usecases.shift import ShiftPostUseCase
from fastapi import APIRouter, Depends
from schemas.shift import ShiftCreate, ShiftDisplay
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return ShiftPostUseCase(ShiftRepository(db),
                           UserRepository(db),
                           GroupRepository(db),
                           TaskRepository(db))

@router.post("/", response_model=ShiftDisplay)
async def shift_post(request:ShiftCreate,
                    user:UserEntity=Depends(get_current_active_user),
                    usecase:ShiftPostUseCase=Depends(__usecase_di)):
    response=usecase.execute(request.name,request.start_time,user.id,request.task_id).to_dict()
    return response
    
