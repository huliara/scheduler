import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TemplateSlotBase(BaseModel):
    task_id: UUID
    date_from_start: int
    start_time: datetime.time
    def __hash__(self):
        return hash(
            (
                self.task_id,
                self.date_from_start,
                self.start_time.hour,
                self.start_time.minute,
            )
        )

    class Config:
        from_attributes = True
        

class TemplateSlot(TemplateSlotBase):
    id:str

class TemplateSlotDisplay(TemplateSlot):
    name:str

class TemplateDisplay(BaseModel):
    id: UUID
    name: str
    group_id: UUID
    group_name: str|None=None
    slots: list[TemplateSlotDisplay]


class TemplatePatchSlot(BaseModel):
    src:TemplateSlotBase
    dst:TemplateSlotBase


class TemplateCreateBase(BaseModel):
    name:str = Field(max_length=20)

class TemplateCreate(TemplateCreateBase):
    slots: list[TemplateSlotBase]
    group_id:UUID

    class Config:
        from_attributes = True

class TaskFromTemplate(BaseModel):
    start_day: datetime.date
    add_default_worker:bool=False
    group_id:UUID|None=None
    class Config:
        from_attributes = True
