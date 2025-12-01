from database import get_db
from ddd.infra.repository import UserRepository
from ddd.service.usecases.user import UserGetAllUseCase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return UserGetAllUseCase(db,UserRepository(db))

@router.get("/users")
async def get_users(usecase:UserGetAllUseCase=Depends(__usecase_di)):
    users=usecase.execute(group_id=None)
    response=[user.to_dict() for user in users]
    return {"users":response}