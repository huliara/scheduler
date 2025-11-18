from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.cruds.auth import get_current_active_user
from app.database import get_db
from app.ddd.infra.repository import (GroupRepository, TaskRepository,
                                      UserRepository)
from app.ddd.service.usecases.user import UserRelateTaskUseCase
from app.models.models import User

router=APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return UserRelateTaskUseCase(db,UserRepository(db),
                          TaskRepository(db),
                          GroupRepository(db))


@router.get("/taskdetails",status_code=200)
async def get_user_relate_taskdetails(user:User=Depends(get_current_active_user),
                               usecase:UserRelateTaskUseCase=Depends(__usecase_di)):
    data=usecase.execute(user.id)
    return [taskdetail.to_dict() for taskdetail in data]
