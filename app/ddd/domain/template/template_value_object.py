import datetime
from dataclasses import dataclass
from typing import NewType
from uuid import UUID

from app.ddd.domain.task_detail import TaskDetailId

TemplateId = NewType('TemplateId', UUID)

@dataclass(frozen=True)
class TemplateSlot:
    taskdetail_id:TaskDetailId
    date_from_start:int
    start_time:datetime.time
    def __post_init__(self):
        if self.date_from_start<0:
            raise ValueError('date_from_start must be positive')
 