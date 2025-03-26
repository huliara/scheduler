from dataclasses import dataclass

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.cruds.auth import get_current_active_user
from app.database import get_db
from app.ddd.domain.user import UserEntity
from app.ddd.infra.repository import UserRepository
from app.ddd.service.usecases.user import UserUpdateParams, UserUpdateUseCase
from app.models.models import User
from app.schemas.users import UserUpdate

router=APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return UserUpdateUseCase(db,UserRepository(db))



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
