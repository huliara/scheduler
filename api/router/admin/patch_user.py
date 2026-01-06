from database import get_db
from ddd.domain.user.user_entity import UserEntity
from ddd.infra.repository import UserRepository
from ddd.service.usecases.user import AdminUserUpdateUseCase
from fastapi import APIRouter, Depends
from schemas.users import AdminUserPatch
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return AdminUserUpdateUseCase(db,UserRepository(db))

@router.patch("/users/{user_id}")
async def patch_user(user_id:str,request:AdminUserPatch,usecase:AdminUserUpdateUseCase=Depends(__usecase_di)):
    user_entity=UserEntity.from_params({
        'id':user_id,
        'name':request.name,
        'room_number':request.room_number,
        'exp_task':[],
        'point':request.point,
    })
    user=usecase.execute(user_entity).to_dict()
    return user