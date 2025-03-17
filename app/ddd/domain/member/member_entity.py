import uuid
from dataclasses import dataclass
from typing import NewType

from app.ddd.core.i_entity import IEntity
from app.ddd.domain.group.group_value_object import GroupId
from app.ddd.domain.user.user_entity import UserEntity
from app.models.models import GroupUser


@dataclass(frozen=True)
class MemberEntity(IEntity):
    user:UserEntity
    group_id:GroupId
    point:float
    def from_model(cls, data: GroupUser) -> 'MemberEntity':
        return cls(
            user=data.user,
            group_id=data.group_id,
            point=data.point
        )
    def to_dict(self):
        return {
            'user': self.user.to_dict(),
            'group_id': self.group_id,
            'point': self.point
        }