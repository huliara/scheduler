import datetime
from uuid import UUID

from pydantic import BaseModel, Field


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


class TaskDisplay(TaskCreate):
    id: UUID
    end_time: datetime.datetime
    creater_id: UUID
    creater_name: str
    assignees: list[Worker] = []
    task_name: str

    class Config:
        from_attributes = True


class TaskList(BaseModel):
    slots: list[TaskDisplay]

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