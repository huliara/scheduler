import datetime
from dataclasses import dataclass, field
from http import HTTPStatus as status

import app.ddd.domain.group as group
import app.ddd.domain.user.user_entity as user
import app.models.models as models
from app.ddd.core.exception import DomainException
from app.ddd.core.i_entity import IEntity
from app.ddd.domain.task_detail.task_detail_entity import TaskDetailEntity
from app.ddd.domain.user.user_value_object import UserId

from .task_state import TaskState
from .task_value_object import TaskId


@dataclass
class TaskEntity(IEntity):
    id:TaskId|None
    name:str
    start_time:datetime.datetime
    status:TaskState
    taskdetail:TaskDetailEntity|None
    workers:list['user.UserEntity']=field(default_factory=list)
    creater_id:UserId|None=None
    @property
    def end_time(self) -> datetime.datetime:
        return self.start_time + self.taskdetail.duration
    @property
    def group_id(self)->'group.GroupId':
        return self.taskdetail.group_id
    @classmethod
    def from_model(cls, data: "models.Task") -> 'TaskEntity':
        return cls(
            id=data.id,
            name=data.name,
            start_time=data.start_time,
            status=data.status,
            workers=[user for user in data.workers],
            taskdetail=TaskDetailEntity.from_model(data.taskdetail),
            creater_id=data.creater_id,
        )
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'status': self.status,
            'taskdetail': self.taskdetail.to_dict(),
            'workers': [user.to_dict() for user in self.workers],
            'creater_id': self.creater_id,
        }
        
    def add(self,user:'user.UserEntity'):
        if self.end_time < datetime.datetime.now():
            raise DomainException(status_code=status.CONFLICT,description='この仕事は既に終了しています')

        exp_assignees = list(filter(lambda x: self.taskdetail.id in x.exp_tasks, self.workers))
        if len(self.workers)>= self.taskdetail.max_worker:
            raise DomainException(status_code=status.CONFLICT,description='この仕事は定員に達しています')
        if (self.taskdetail.id not in user.exp_tasks) and self.taskdetail.max_worker - len(
            self.workers
        ) + len(exp_assignees) <= self.taskdetail.exp_worker:
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
            raise DomainException(status_code=status.CONFLICT,description='このユーザーは参加していません')
        self.status=TaskState.archive
        return self
    