from database import get_db
from ddd.domain.user import UserEntity
from ddd.infra.repository import UserRepository
from ddd.service.usecases.user import UserPostUseCase
from fastapi import APIRouter, Depends
from schemas.auth import Token
from schemas.users import UserCreate
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return UserPostUseCase(UserRepository(db))


@router.post("/signup", response_model=Token)
async def post_users(request:UserCreate,usecase:UserPostUseCase=Depends(__usecase_di)):

    user_entity=UserEntity.from_params(request.model_dump(exclude={"password"}))
    user=usecase.execute(user_entity,request.password).to_dict()
    return user
