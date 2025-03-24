from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.domain.user import UserEntity
from app.ddd.infra.repository import UserRepository
from app.ddd.service.usecases.user import AdminUserUpdateUseCase
from app.schemas.users import AdminUserPatch

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