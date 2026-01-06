from database import get_db
from ddd.domain.user.user_entity import UserEntity
from ddd.infra.auth import get_current_active_user
from ddd.infra.repository import UserRepository
from ddd.service.usecases.user import UserUpdatePasswordUseCase
from fastapi import APIRouter, Depends
from schemas.users import UserUpdatePassword
from sqlalchemy.orm import Session

router=APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return UserUpdatePasswordUseCase(UserRepository(db))


@router.patch("/password",status_code=200)
async def update_user_password(request:UserUpdatePassword,
                               user:UserEntity=Depends(get_current_active_user),
                               usecase:UserUpdatePasswordUseCase=Depends(__usecase_di)):
    usecase.execute(user.id,request.password)
    return {"message":"password updated"}
