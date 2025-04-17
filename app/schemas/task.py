import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.ddd.domain.task.task_state import TaskState

from .taskdetail import TaskDetailDisplay


class TaskCreate(BaseModel):
    name: str = Field(max_length=20)
    start_time: datetime.datetime
    taskdetail_id: UUID

    class Config:
        from_attributes = True


class TaskDeleteRequest(BaseModel):
    slots_id: list[UUID]


class Worker(BaseModel):
    id: UUID
    name: str

class ResponseBase(BaseModel):
    id: UUID
    name: str


    class Config:
        from_attributes = True

class TaskDisplay(BaseModel):
    id: UUID
    name:str
    start_time: datetime.datetime
    end_time: datetime.datetime
    status:TaskState
    taskdetail:ResponseBase
    workers: list[Worker] = []
    creater_id: UUID|None=None
    group_id:UUID

    class Config:
        from_attributes = True


class TaskList(BaseModel):
    tasks: list[TaskDisplay]

    class Config:
        from_attributes = True

class UserTaskList(BaseModel):
    assign: list[TaskDisplay]
    hiring: list[TaskDisplay]
    end: list[TaskDisplay]

    class Config:
        from_attributes = True

class TaskDelete(BaseModel):
    tasks: list[UUID]

    class Config:
        from_attributes = True

class TaskComplete(BaseModel):
    done: bool
    class Config:
        from_attributes = True