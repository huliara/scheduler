from database import get_db
from ddd.infra.repository import UserRepository
from ddd.service.usecases.user import UserRemoveUseCase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return UserRemoveUseCase(db,UserRepository(db))

@router.delete("/users/{user_id}")
async def delete_user(user_id:str,usecase:UserRemoveUseCase=Depends(__usecase_di)):
    user=usecase.execute(user_id).to_dict()
    return user