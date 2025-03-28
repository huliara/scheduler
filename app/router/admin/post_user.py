from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.domain.user import UserEntity
from app.ddd.infra.repository import UserRepository
from app.ddd.service.usecases.user import UserPostUseCase
from app.schemas.users import AdminUserCreate

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return UserPostUseCase(db,UserRepository(db))

@router.post("/users")
async def post_users(request:AdminUserCreate,usecase:UserPostUseCase=Depends(__usecase_di)):
    params={
        "name":request.name,
        "room_number":request.room_number,
        "exp_task":[],
        "is_admin":request.is_admin
    }
    user_entity=UserEntity.from_params(params)
    user=usecase.execute(user_entity,request.password).to_dict()
    return user

