from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.domain.user import UserEntity
from app.ddd.infra.auth import get_current_active_user
from app.ddd.infra.repository import ShiftRepository, UserRepository
from app.ddd.service.usecases.shift import ShiftGetUserRelevantUseCase
from app.schemas.shift import UserShiftList

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return ShiftGetUserRelevantUseCase(ShiftRepository(db))

def to_response(task):
    return {
        "id": task["id"],
        "name": task["name"],
        "start_time": task["start_time"],
        "end_time": task["end_time"],
        "status": task["status"],
        "taskdetail": {
            "id": task["taskdetail"]["id"],
            "name": task["taskdetail"]["name"],
        },
        "workers": [
            {
                "id": worker["id"],
                "name": worker["name"],
            }
            for worker in task["workers"]
        ],
        "creater_id": task['creater_id'],
        "group_id": task['group_id'],
    }

@router.get("/shifts", response_model=UserShiftList)
async def get_shifts_relevant_user(user:UserEntity=Depends(get_current_active_user),
                                 usecase:ShiftGetUserRelevantUseCase=Depends(__usecase_di)):
    shifts=usecase.execute(user.id)
    assign_tasks_dict=[task.to_dict() for task in shifts["assign"] ]
    hiring_tasks_dict=[task.to_dict() for task in shifts['hiring'] ]
    end_tasks_dict=[task.to_dict() for task in shifts["end"]]
    response={
        "assign":[to_response(task) for task in assign_tasks_dict],
        "hiring":[to_response(task) for task in hiring_tasks_dict],
        "end":[to_response(task) for task in end_tasks_dict],
    }
    return response
    
