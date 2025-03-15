
from dataclasses import dataclass

from app.ddd.core.i_entity import IEntity
from app.ddd.domain.task.task_value_object import TaskId
from app.ddd.domain.task_detail.task_detail_entity import TaskDetailEntity
from app.ddd.domain.user.user_value_object import UserId
from app.models.models import User


@dataclass
class UserEntity(IEntity):
    id:UserId|None
    name:str
    room_number:str
    tasks:list[TaskId]
    exp_tasks:list[TaskDetailEntity]
    point:int=0
    @classmethod
    def from_model(cls, data: User) -> 'UserEntity':
        return cls(
            id=data.id,
            name=data.name,
            tasks=[task.id for task in data.tasks],
            exp_tasks=[TaskDetailEntity.from_model(task_detail) for task_detail in data.exp_tasks],
            point=data.point
        )
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'tasks': self.tasks,
            'exp_tasks': [task.to_dict() for task in self.exp_tasks],
            'point': self.point
        }
    def add(self,task:TaskId):
        self.tasks.append(task)