from database import get_db
from ddd.infra.repository import UserRepository
from ddd.service.usecases.user import AdminUserAdminateUseCase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return AdminUserAdminateUseCase(db,UserRepository(db))

@router.patch("/users/{user_id}")
async def adminate_user(user_id:str,admin:bool,usecase:AdminUserAdminateUseCase=Depends(__usecase_di)):
    user=usecase.execute(user_id,admin).to_dict()
    return user