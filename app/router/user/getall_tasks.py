from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.cruds.auth import get_current_active_user
from app.database import get_db
from app.ddd.infra.repository import TaskRepository, UserRepository
from app.ddd.service.usecases.task import TaskGetUserRelevantUseCase
from app.models.models import User
from app.schemas.task import UserTaskList

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TaskGetUserRelevantUseCase(db,TaskRepository(db),UserRepository(db))

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

@router.get("/tasks", response_model=UserTaskList)
async def get_task_relevant_user(user:User=Depends(get_current_active_user),
                                 usecase:TaskGetUserRelevantUseCase=Depends(__usecase_di)):
    tasks=usecase.execute(user.id)
    assign_tasks_dict=[task.to_dict() for task in tasks["assign"] ]
    hiring_tasks_dict=[task.to_dict() for task in tasks['hiring'] ]
    end_tasks_dict=[task.to_dict() for task in tasks["end"]]
    response={
        "assign":[to_response(task) for task in assign_tasks_dict],
        "hiring":[to_response(task) for task in hiring_tasks_dict],
        "end":[to_response(task) for task in end_tasks_dict],
    }
    return response
    
