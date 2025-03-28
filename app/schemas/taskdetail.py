from datetime import timedelta
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class TaskDetailBase(BaseModel):
    name: str = Field(max_length=20)
    detail: str = Field(max_length=400)
    max_worker_num: int = Field(default=1, gte=1)
    min_worker_num: int = Field(default=1, gte=0)
    exp_worker_num: int = Field(default=0, gte=0)
    point: int = Field(0, gt=0)
    @model_validator(pre=True)
    def validate_worker_num(cls, values):
        if int(values["max_worker_num"]) < int(values["min_worker_num"]):
            raise ValueError("Be sure that the max worker is greater than min worker.")
        if int(values["exp_worker_num"]) > int(values["min_worker_num"]):
            raise ValueError("Be sure that the exp worker is less than min worker.")
        return values

class TaskDetailCreate(TaskDetailBase):
    duration: timedelta



class TaskDetailDisplay(TaskDetailBase):
    id: UUID
    creater_id: UUID
    creater_name: str
    group_id: UUID
    duration: int

    class Config:
        from_attributes = True


class TaskDetailList(BaseModel):
    tasks: list[TaskDetailDisplay]

    class Config:
        from_attributes = True
