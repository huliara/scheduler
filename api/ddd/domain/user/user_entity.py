
from dataclasses import dataclass, field

import models.models as models
from ddd.core.i_entity import IEntity
from ddd.domain.shift.shift_value_object import ShiftId
from ddd.domain.task.task_value_object import TaskId
from .user_value_object import UserId


@dataclass
class UserEntity(IEntity):
    id:UserId|None
    name:str
    room_number:str
    exp_tasks:list[TaskId]
    shifts:list[ShiftId]=field(default_factory=list)
    point:int=0
    is_admin:bool=False
    is_active:bool=True
    @classmethod
    def from_params(cls,data:dict) -> 'UserEntity':
        return cls(
            id=UserId(data['id']) if 'id'in data.keys() is not None else None,
            name=data['name'],
            room_number=data['room_number'],
            exp_tasks=data['exp_tasks'],
            is_admin=data['is_admin'] if 'is_admin' in data else False,
            is_active=data['is_active'] if 'is_active' in data else True,
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
            shifts=[task.id for task in data.shifts],
            exp_tasks=[task.id for task in data.exp_tasks],
            point=data.point,
            is_admin=data.is_admin,
            is_active=data.is_active,
        )
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'room_number': self.room_number,
            'shifts': self.shifts,
            'exp_tasks': [task for task in self.exp_tasks],
            'point': self.point,
            'is_active': self.is_active,
        }
    def add_shift(self,shift:ShiftId):
        self.shifts.append(shift)
    def add_exp(self,task:TaskId):
        self.exp_tasks.append(task)
    