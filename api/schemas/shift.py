import datetime
from uuid import UUID

from pydantic import BaseModel, Field
from schemas.task import TaskDisplay


class ShiftCreate(BaseModel):
    name: str = Field(max_length=20)
    start_time: datetime.datetime
    task_id: UUID

    class Config:
        from_attributes = True


class ShiftDeleteRequest(BaseModel):
    slots_id: list[UUID]


class Worker(BaseModel):
    id: UUID
    name: str

class ResponseBase(BaseModel):
    id: UUID
    name: str


    class Config:
        from_attributes = True

class ShiftDisplay(BaseModel):
    id: UUID
    name:str
    start_time: datetime.datetime
    end_time: datetime.datetime
    task: TaskDisplay
    workers: list[Worker] = []
    creater_id: UUID|None=None
    group_id:UUID
    group_name:str|None=None
    class Config:
        from_attributes = True



    class Config:
        from_attributes = True


class ShiftsDelete(BaseModel):
    shifts: list[UUID]
    class Config:
        from_attributes = True

class ShiftComplete(BaseModel):
    done: bool
    latitude: float
    longitude: float
    class Config:
        from_attributes = True
        
class ShiftWorkerReplace(BaseModel):
    new_worker_id: UUID
    class Config:
        from_attributes = True