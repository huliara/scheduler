import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.ddd.domain.shift.shift_state import ShiftState

from .task import TaskDisplay


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
    status:ShiftState
    taskdetail:ResponseBase
    workers: list[Worker] = []
    creater_id: UUID|None=None
    group_id:UUID

    class Config:
        from_attributes = True


class ShiftList(BaseModel):
    tasks: list[ShiftDisplay]

    class Config:
        from_attributes = True

class UserShiftList(BaseModel):
    assign: list[ShiftDisplay]
    hiring: list[ShiftDisplay]
    end: list[ShiftDisplay]

    class Config:
        from_attributes = True

class ShiftDelete(BaseModel):
    shifts: list[UUID]
    group_id:UUID|None=None

    class Config:
        from_attributes = True

class ShiftComplete(BaseModel):
    done: bool
    class Config:
        from_attributes = True