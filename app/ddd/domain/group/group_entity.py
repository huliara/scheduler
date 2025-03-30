from dataclasses import dataclass

from app.ddd.core.i_entity import IEntity
from app.ddd.domain.member.member_entity import MemberEntity
from app.ddd.domain.task_detail.task_detail_entity import TaskDetailId
from app.ddd.domain.template.template_entity import TemplateId
import app.models.models as models
from .group_value_object import GroupId


@dataclass
class GroupEntity(IEntity):
    id:GroupId|None
    name:str
    users:list[MemberEntity]
    task_details:list[TaskDetailId]
    template:list[TemplateId]
    @classmethod
    def from_model(cls, data: "models.Group") -> 'GroupEntity':
        return cls(
            id=data.id,
            name=data.name,
            users=[MemberEntity.from_model(user) for user in data.users],
            task_details=[task_detail.id for task_detail in data.taskdetail],
            template=[template.id for template in data.templates]
        )
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'users': [user.to_dict() for user in self.users],
            'task_details': self.task_details,
            'template': self.template
        }