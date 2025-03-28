import datetime
from dataclasses import dataclass, field
from http import HTTPStatus as status

from app.ddd.core.exception import DomainException
from app.ddd.core.i_entity import IEntity
from app.ddd.domain.group.group_value_object import GroupId
from app.ddd.domain.task.task_state import TaskState
from app.ddd.domain.task.task_value_object import TaskId
from app.ddd.domain.task_detail.task_detail_entity import TaskDetailEntity
from app.ddd.domain.user.user_entity import UserEntity
from app.ddd.domain.user.user_value_object import UserId
from app.models.models import Task


@dataclass
class TaskEntity(IEntity):
    id:TaskId|None
    name:str
    start_time:datetime.datetime
    status:TaskState
    taskdetail:TaskDetailEntity
    workers:list[UserEntity]=field(default_factory=list)
    creater_id:UserId|None=None
    @property
    def end_time(self) -> datetime.datetime:
        return self.start_time + self.taskdetail.duration
    @property
    def group_id(self) -> GroupId:
        return self.taskdetail.group_id
    @classmethod
    def from_model(cls, data: Task) -> 'TaskEntity':
        return cls(
            id=data.id,
            name=data.name,
            start_time=data.start_time,
            end_time=data.end_time,
            status=data.status,
            assignees=[user.id for user in data.workers],
            taskdetail=TaskDetailEntity.from_model(data.taskdetail)
        )
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'status': self.status,
            'assignees': self.workers,
            'taskdetail': self.taskdetail.to_dict()
        }
        
    def add(self,user:UserEntity):
        if self.end_time < datetime.datetime.now():
            raise DomainException(status_code=status.CONFLICT,message='この仕事は既に終了しています')

        exp_assignees = list(filter(lambda x: self.taskdetail in x.exp_tasks, self.workers))
        if len(self.workers)>= self.taskdetail.max_worker:
            raise DomainException(status_code=status.CONFLICT)
        if (self.taskdetail not in user.exp_tasks) and self.taskdetail.max_worker - len(
            self.workers
        ) + len(exp_assignees) <= self.taskdetail.exp_worker:
            raise DomainException(status_code=status.CONFLICT)
        self.workers.append(user)
        return self
    
    def remove(self,user:UserEntity):
        if user not in self.workers:
            raise DomainException(status_code=status.CONFLICT)
        self.workers.remove(user)
        return self
    
    def complete(self,user:UserEntity):
        if user not in self.workers:
            raise DomainException(status_code=status.CONFLICT)
        self.status=TaskState.archive
        return self
    