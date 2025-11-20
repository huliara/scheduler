from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.domain.user import UserEntity
from app.ddd.infra.auth import get_current_active_user
from app.ddd.infra.repository import (GroupRepository, ShiftRepository,
                                      TaskRepository, UserRepository)
from app.ddd.service.usecases.shift import ShiftPostUseCase
from app.schemas.shift import ShiftCreate, ShiftDisplay

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
    
