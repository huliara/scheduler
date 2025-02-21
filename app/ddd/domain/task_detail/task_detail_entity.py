import datetime
from dataclasses import dataclass, field

from app.ddd.core.i_entity import IEntity
from app.ddd.domain.group.group_value_object import GroupId
from app.ddd.domain.permission.permission import Permission
from app.ddd.domain.task_detail.task_detail_value_object import TaskDetailId
from app.ddd.domain.user import UserId
from app.models.models import TaskDetail


@dataclass
class TaskDetailEntity(IEntity):
    id: TaskDetailId|None
    name: str
    max_worker: int
    min_worker: int
    exp_worker: int
    duration: datetime.timedelta
    group_id:GroupId
    permissions: list[Permission]=field(default_factory=list)
    wage: int=0
    subtask:list[str]=field(default_factory=list)
    creater_id:UserId
    def from_model(cls,data:TaskDetail) -> 'TaskDetailEntity':
        return cls(
            id=TaskDetailId(data.id),
            name=data.name,
            subtask=[subtask.description for subtask in data.subtask],
            max_assignees=data.max_worker,
            min_assignees=data.min_worker,
            exp_assignees=data.exp_worker,
            wage=data.wage,
            duration=data.duration,
            permissions=[permission for permission in data.permissions]
        )
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'subtask': [{'order':index,'decription':subtask} for index,subtask in enumerate(self.subtask)],
            'max_assignees': self.max_worker,
            'min_assignees': self.min_worker,
            'exp_assignees': self.exp_worker,
            'wage': self.wage,
            'duration': self.duration,
            'permissions': [permission for permission in self.permissions]
        }
