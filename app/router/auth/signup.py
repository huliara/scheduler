from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.domain.user import UserEntity
from app.ddd.infra.repository import UserRepository
from app.ddd.service.usecases.user import UserPostUseCase
from app.schemas.auth import Token
from app.schemas.users import UserCreate

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return UserPostUseCase(UserRepository(db))


@router.post("/signup", response_model=Token)
async def post_users(request:UserCreate,usecase:UserPostUseCase=Depends(__usecase_di)):

    user_entity=UserEntity.from_params(request.model_dump(exclude={"password"}))
    user=usecase.execute(user_entity,request.password).to_dict()
    return user
