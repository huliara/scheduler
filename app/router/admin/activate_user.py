from database import get_db
from ddd.infra.repository import UserRepository
from ddd.service.usecases.user import AdminUserActivateUseCase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return AdminUserActivateUseCase(UserRepository(db))

@router.patch("/users/{user_id}")
async def activate_user(user_id:str,activate:bool,usecase:AdminUserActivateUseCase=Depends(__usecase_di)):
    user=usecase.execute(user_id,activate).to_dict()
    return user