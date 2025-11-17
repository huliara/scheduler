import datetime
from dataclasses import dataclass
from typing import NewType
from uuid import UUID

from app.ddd.domain.task import TaskId

TemplateId = NewType('TemplateId', UUID)

@dataclass(frozen=True)
class TemplateSlot:
    taskdetail_id:TaskId
    taskdetail_name:str
    date_from_start:int
    start_time:datetime.time
    @property
    def name(self):
        return f'{self.date_from_start+1}_{self.start_time}_{self.taskdetail_name}'
    def __post_init__(self):
        if self.date_from_start<0:
            raise ValueError('date_from_start must be positive')
 