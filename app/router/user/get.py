from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from ddd.infra.auth import get_current_active_user
from ddd.infra.repository import UserRepository
from ddd.service.usecases.user import UserGetUseCase
from models.models import User

router=APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return UserGetUseCase(UserRepository(db))


@router.get("/profile",status_code=200)
async def get_user_profile(user:User=Depends(get_current_active_user),
                               usecase:UserGetUseCase=Depends(__usecase_di)):
    user=usecase.execute(user.id).to_dict()
    return user
