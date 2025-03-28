import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TemplateSlot(BaseModel):
    id: UUID
    name: str
    date_from_start: int
    start_time: datetime.time

    class Config:
        from_attributes = True


class TemplateDisplay(BaseModel):
    id: UUID
    name: str
    group_id: UUID
    slots: list[TemplateSlot]


class TemplateList(BaseModel):
    templates: list[TemplateDisplay]

    class Config:
        from_attributes = True


class TemplateTaskBase(BaseModel):
    id: UUID
    date_from_start: int=Field(ge=0)
    start_time: datetime.time

    def __hash__(self):
        return hash(
            (
                self.id,
                self.date_from_start,
                self.start_time.hour,
                self.start_time.minute,
            )
        )

    class Config:
        from_attributes = True


class TemplateCreateBase(BaseModel):
    name:str = Field(max_length=20)

class TemplateCreate(TemplateCreateBase):
    slots: set[TemplateTaskBase] = set()

    class Config:
        from_attributes = True

class TaskFromTemplate(BaseModel):
    start_day: datetime.date
    add_default_worker:bool=False

    class Config:
        from_attributes = True
