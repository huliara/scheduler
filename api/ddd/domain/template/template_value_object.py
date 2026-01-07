import datetime
from dataclasses import dataclass
from typing import NewType
from uuid import UUID

from ddd.domain.task.task_value_object import TaskId

TemplateId = NewType('TemplateId', UUID)

@dataclass(frozen=True)
class TemplateSlot:
    task_id:TaskId
    date_from_start:int
    start_time:datetime.time
    task_name:str|None=None
    @property
    def name(self):
        return f'{self.date_from_start}_{self.start_time}_{self.task_name}'
    def __post_init__(self):
        if self.date_from_start<0:
            raise ValueError('date_from_start must be positive')
    def to_dict(self):
        return {
            'task_id': self.task_id,
            'task_name': self.task_name,
            'name': self.name,
            'date_from_start': self.date_from_start,
            'start_time': self.start_time,
        }
    def __hash__(self):
        return hash((self.task_id,self.date_from_start,self.start_time))
    def __eq__(self,other):
        if not isinstance(other,TemplateSlot):
            return False
        return (self.task_id==other.task_id and
                self.date_from_start==other.date_from_start and
                self.start_time==other.start_time)