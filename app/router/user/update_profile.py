from database import get_db
from ddd.infra.auth import get_current_active_user
from ddd.infra.repository import TaskRepository, UserRepository
from ddd.service.usecases.user import UserUpdateParams, UserUpdateUseCase
from fastapi import APIRouter, Depends
from models.models import User
from schemas.users import UserUpdate
from sqlalchemy.orm import Session

router=APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return UserUpdateUseCase(UserRepository(db),TaskRepository(db))



@router.patch("/profile")
async def update_user_profile(request:UserUpdate,user:User=Depends(get_current_active_user),usecase:UserUpdateUseCase=Depends(__usecase_di)):
    param= UserUpdateParams(
        id=user.id,
        name=request.name,
        room_number=request.room_number,
        exp_tasks=request.exp_task
    )
    user=usecase.execute(param).to_dict()
    return user
