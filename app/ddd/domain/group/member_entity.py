import uuid
from dataclasses import dataclass
from typing import NewType

from app.ddd.core.i_entity import IEntity
from app.ddd.domain.group.group_value_object import GroupId
from app.ddd.domain.user.user_entity import UserId
from app.models.models import GroupUser


@dataclass(frozen=True)
class MemberEntity(IEntity):
    id:UserId
    group_id:GroupId
    point:float
    def from_model(cls, data: GroupUser) -> 'MemberEntity':
        return cls(
            id=data.id,
            group_id=data.group_id,
            point=data.point
        )
    def to_dict(self):
        return {
            'id': self.id,
            'group_id': self.group_id,
            'point': self.point
        }