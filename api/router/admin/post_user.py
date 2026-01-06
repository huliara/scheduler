from database import get_db
from ddd.domain.user.user_entity import UserEntity
from ddd.infra.repository import UserRepository
from ddd.service.usecases.user import UserPostUseCase
from fastapi import APIRouter, Depends
from schemas.users import AdminUserCreate
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return UserPostUseCase(db,UserRepository(db))

@router.post("/users")
async def post_users(request:AdminUserCreate,usecase:UserPostUseCase=Depends(__usecase_di)):
    params={
        "name":request.name,
        "room_number":request.room_number,
        "exp_tasks":[],
        "is_admin":request.is_admin
    }
    user_entity=UserEntity.from_params(params)
    user=usecase.execute(user_entity,request.password).to_dict()
    return user

