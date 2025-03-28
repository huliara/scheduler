from dataclasses import dataclass

import app.ddd.domain.group as group
from app.ddd.core.i_entity import IEntity
from app.ddd.domain.user.user_value_object import UserId
from app.models.models import GroupUser


@dataclass
class MemberEntity(IEntity):
    user_id:UserId
    group_id:'group.GroupId'
    point:float
    def from_model(cls, data: GroupUser) -> 'MemberEntity':
        return cls(
            user=data.user_id,
            group_id=data.group_id,
            point=data.point
        )
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'group_id': self.group_id,
            'point': self.point
        }