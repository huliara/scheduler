
from dataclasses import dataclass

from app.ddd.core.i_entity import IEntity
from app.ddd.domain.task.task_value_object import TaskId
from app.ddd.domain.task_detail.task_detail_value_object import TaskDetailId
from .user_value_object import UserId
import app.models.models as models


@dataclass
class UserEntity(IEntity):
    id:UserId|None
    name:str
    room_number:str
    tasks:list[TaskId]
    exp_tasks:list[TaskDetailId]
    point:int=0
    is_admin:bool=False
    is_active:bool=True
    @classmethod
    def from_params(cls,data:dict) -> 'UserEntity':
        return cls(
            id=UserId(data['id']) if data['id'] is not None else None,
            name=data['name'],
            room_number=data['room_number'],
            exp_tasks=data['exp_tasks'],
            is_admin=data['is_admin'] if 'is_admin' in data else False,
            point=data['point'] if 'point' in data else 0
        )
    def update_profile(self,data:dict):
        self.name=data['name']
        self.room_number=data['room_number']
        self.exp_tasks=data['exp_tasks']
        
    @classmethod
    def from_model(cls, data: "models.User") -> 'UserEntity':
        return cls(
            id=data.id,
            name=data.name,
            room_number=data.room_number,
            tasks=[task.id for task in data.tasks],
            exp_tasks=data.exp_tasks,
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
    