import datetime
from dataclasses import dataclass, field

import models.models as models
from ddd.core.i_entity import IEntity
from ddd.domain.group.group_value_object import GroupId
from ddd.domain.permission.permission import Permission
from ddd.domain.user.user_value_object import UserId

from .task_value_object import TaskId


@dataclass
class TaskEntity(IEntity):
    id: TaskId|None
    name: str
    max_worker: int
    min_worker: int
    exp_worker: int
    duration: datetime.timedelta
    group_id:GroupId
    creater_id:UserId
    group_name:str|None=None
    permissions: list[Permission]=field(default_factory=list)
    wage: int=0
    subtask:list[str]=field(default_factory=list)
    
    @classmethod
    def from_model(cls,data:"models.Task") -> 'TaskEntity':
        return cls(
            id=TaskId(data.id),
            name=data.name,
            subtask=[subtask.description for subtask in data.subtask],
            max_worker=data.max_worker,
            min_worker=data.min_worker,
            exp_worker=data.exp_worker,
            wage=data.wage,
            duration=data.duration,
            group_id=data.group_id,
            group_name=data.group.name,
            creater_id=data.creater_id,
            permissions=[permission for permission in data.permissions]
        )
    @classmethod
    def from_params(cls, data: dict) -> 'TaskEntity':
        return cls(
            id=TaskId(data['id']),
            name=data['name'],
            subtask=data['subtasks'],
            max_worker=data['max_worker'],
            min_worker=data['min_worker'],
            exp_worker=data['exp_worker'],
            wage=data['wage'],
            duration=datetime.timedelta(minutes=data['duration']),
            group_id=GroupId(data['group_id']),
            permissions=[permission for permission in data['permissions']],
            creater_id=UserId(data['creater_id'])
        )
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'subtasks': self.subtask,
            'max_worker': self.max_worker,
            'min_worker': self.min_worker,
            'exp_worker': self.exp_worker,
            'wage': self.wage,
            'duration': divmod(self.duration.seconds,60)[0],
            'permissions': [permission for permission in self.permissions],
            'creater_id': self.creater_id,
            'group_id': self.group_id,
            'group_name': self.group_name,
        }
