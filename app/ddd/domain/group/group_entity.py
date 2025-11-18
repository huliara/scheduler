from dataclasses import dataclass, field

import app.models.models as models
from app.ddd.core.i_entity import IEntity
from app.ddd.domain.member.member_entity import MemberEntity
from app.ddd.domain.task.task_entity import TaskId
from app.ddd.domain.template.template_entity import TemplateId

from .group_value_object import GroupId


@dataclass
class GroupEntity(IEntity):
    id:GroupId|None
    name:str
    users:list[MemberEntity]=field(default_factory=list)
    task:list[TaskId]=field(default_factory=list)
    template:list[TemplateId]=field(default_factory=list)
    @classmethod
    def from_model(cls, data: "models.Group") -> 'GroupEntity':
        return cls(
            id=data.id,
            name=data.name,
            users=[MemberEntity.from_model(user) for user in data.users],
            tasks=[task.id for task in data.tasks],
            template=[template.id for template in data.templates]
        )
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'users': [{'id':user.user_id,'point':user.point} for user in self.users],
            'task': self.task,
            'template': self.template
        }