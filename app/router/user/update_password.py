from dataclasses import dataclass

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.cruds.auth import get_current_active_user
from app.database import get_db
from app.ddd.domain.user import UserEntity
from app.ddd.infra.repository import UserRepository
from app.ddd.service.usecases.user import UserUpdatePasswordUseCase
from app.models.models import User
from app.schemas.users import UserUpdatePassword

router=APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return UserUpdatePasswordUseCase(db,UserRepository(db))


@router.patch("/password",status_code=200)
async def update_user_password(request:UserUpdatePassword,
                               user:User=Depends(get_current_active_user),
                               usecase:UserUpdatePasswordUseCase=Depends(__usecase_di)):
    usecase.execute(user.id,request.password)
    return {"message":"password updated"}
