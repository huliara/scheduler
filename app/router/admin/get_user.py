from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import UserRepository
from app.ddd.service.usecases.user import UserGetUseCase

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return UserGetUseCase(db,UserRepository(db))

@router.get("/users/{user_id}")
async def get_user(user_id:str,usecase:UserGetUseCase=Depends(__usecase_di)):
    user=usecase.execute(user_id).to_dict()
    return user