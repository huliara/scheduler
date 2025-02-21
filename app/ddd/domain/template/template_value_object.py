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
    def __init__(self,
                 taskdetail_id:TaskDetailId,
                 date_from_start:int,
                 start_time:datetime.time):
        if date_from_start<0:
            raise ValueError('date_from_start must be positive')
        self.taskdetail_id=taskdetail_id
        self.date_from_start=date_from_start
        self.start_time=start_time