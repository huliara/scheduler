from dataclasses import dataclass, field

import ddd.domain.group as group
import models.models as models
from ddd.domain.task.task_value_object import TaskId
from ddd.domain.user.user_value_object import UserId


@dataclass
class MemberEntity():
    user_id:UserId
    group_id:'group.GroupId'
    is_active:bool=False
    point:float=0.0
    exp_tasks:list[TaskId]=field(default_factory=list)
    @classmethod
    def from_model(cls, data: "models.GroupUser") -> 'MemberEntity':
        return cls(
            user_id=data.user_id,
            group_id=data.group_id,
            point=data.point,
            is_active=data.is_active,
            exp_tasks=[task_id.id for task_id in data.exp_tasks]
        )
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'group_id': self.group_id,
            'point': self.point,
            "is_active": self.is_active     
        }