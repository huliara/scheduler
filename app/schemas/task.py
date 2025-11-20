from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from app.ddd.domain.permission.permission import Permission


class TaskBase(BaseModel):
    name: str = Field(max_length=20)
    subtasks: list[str] = Field(default_factory=list)
    max_worker: int = Field(default=1, gte=1)
    min_worker: int = Field(default=1, gte=0)
    exp_worker: int = Field(default=0, gte=0)
    wage: int = Field(0, gt=0)
    permissions: list[Permission] = Field(default_factory=list)
    @model_validator(mode="before")
    def validate_worker_num(cls, values):
        if int(values["max_worker"]) < int(values["min_worker"]):
            raise ValueError("Be sure that the max worker is greater than min worker.")
        if int(values["exp_worker"]) > int(values["min_worker"]):
            raise ValueError("Be sure that the exp worker is less than min worker.")
        return values

class TaskCreate(TaskBase):
    group_id: UUID
    duration: int #分単位

class TaskDisplay(TaskBase):
    id: UUID
    creater_id: UUID
    group_id: UUID
    duration: int

    class Config:
        from_attributes = True


class TaskList(BaseModel):
    tasks: list[TaskDisplay]

    class Config:
        from_attributes = True
