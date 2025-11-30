from database import get_db
from ddd.infra.auth import get_current_active_user
from ddd.infra.repository import (GroupRepository, TaskRepository,
                                  UserRepository)
from ddd.service.usecases.user import UserRelateTaskUseCase
from fastapi import APIRouter, Depends
from models.models import User
from sqlalchemy.orm import Session

router=APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return UserRelateTaskUseCase(UserRepository(db),
                          TaskRepository(db),
                          GroupRepository(db))


@router.get("/taskdetails",status_code=200)
async def get_user_relate_task(user:User=Depends(get_current_active_user),
                               usecase:UserRelateTaskUseCase=Depends(__usecase_di)):
    data=usecase.execute(user.id)
    return [taskdetail.to_dict() for taskdetail in data]
