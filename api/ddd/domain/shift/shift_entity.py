import datetime
from dataclasses import dataclass, field
from http import HTTPStatus as status

import ddd.domain.group as group
import ddd.domain.user.user_entity as user
import models.models as models
from ddd.core.exception import DomainException
from ddd.core.i_entity import IEntity
from ddd.domain.task.task_entity import TaskEntity
from ddd.domain.user import UserEntity, UserId

from .shift_state import ShiftState
from .shift_value_object import ShiftId


@dataclass
class ShiftEntity(IEntity):
    id:ShiftId|None
    name:str
    start_time:datetime.datetime
    status:ShiftState
    task:TaskEntity
    workers:list['user.UserEntity']=field(default_factory=list)
    creater_id:UserId|None=None
    @property
    def end_time(self) -> datetime.datetime:
        return self.start_time + self.task.duration
    @property
    def group_id(self)->'group.GroupId':
        return self.task.group_id
    @property
    def group_name(self)->str|None:
        return self.task.group_name
    @classmethod
    def from_model(cls, data: "models.Shift") -> 'ShiftEntity':
        return cls(
            id=data.id,
            name=data.name,
            start_time=data.start_time,
            status=data.status,
            workers=[UserEntity.from_model(user) for user in data.workers],
            task=TaskEntity.from_model(data.task),
            creater_id=data.creater_id,
        )
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'status': self.status,
            'task': self.task.to_dict(),
            'workers': [{'id':user.id,'name':user.name} for user in self.workers],
            'creater_id': self.creater_id,
            'group_id': self.group_id,
            'group_name': self.group_name,
        }
        
    def add(self,user:'user.UserEntity'):
        if self.end_time < datetime.datetime.now():
            raise DomainException(status_code=status.CONFLICT,description='この仕事は既に終了しています')

        exp_assignees = list(filter(lambda x: self.task.id in x.exp_tasks, self.workers))
        if len(self.workers)>= self.task.max_worker:
            raise DomainException(status_code=status.CONFLICT,description='この仕事は定員に達しています')
        if (self.task.id not in user.exp_tasks) and self.task.max_worker - len(
            self.workers
        ) + len(exp_assignees) <= self.task.exp_worker:
            raise DomainException(status_code=status.CONFLICT,description='経験書のみ参加できます')
        self.workers.append(user)
        return self
    
    def remove(self,user:'user.UserEntity'):
        if user not in self.workers:
            raise DomainException(status_code=status.CONFLICT,description='このユーザーは参加していません')
        self.workers.remove(user)
        return self
    
    def complete(self,user:'user.UserEntity'):
        if user not in self.workers:
            raise DomainException(status_code=status.CONFLICT,description='無効なシフト枠です')
        self.status=ShiftState.archive
        return self
    