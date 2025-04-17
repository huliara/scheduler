from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.cruds.auth import get_current_active_user
from app.database import get_db
from app.ddd.infra.repository import (GroupRepository, TaskDetailRepository,
                                      UserRepository)
from app.ddd.service.usecases.user import UserGetUseCase
from app.models.models import User

router=APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return UserGetUseCase(db,UserRepository(db),
                          TaskDetailRepository(db),
                          GroupRepository(db))


@router.get("/",status_code=200)
async def get_user_profile(user:User=Depends(get_current_active_user),
                               usecase:UserGetUseCase=Depends(__usecase_di)):
    data=usecase.execute(user.id)
    return {
        'id':data["user"].id,
        "name":data["user"].name,
        "room_number":data["user"].room_number,
        "exp_tasks":[{'id':task.id,'name':task.name} for task in data["taskdetails"]],
        "groups":[{'id':group['id'],'name':group['name']} for group in data["groups"]],
        "is_admin":data["user"].is_admin,
        "is_active":data["user"].is_active,
    }
