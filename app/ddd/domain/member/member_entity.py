from dataclasses import dataclass
from uuid import UUID

import app.ddd.domain.group as group
import app.models.models as models
from app.ddd.core.i_entity import IEntity
from app.ddd.domain.user.user_value_object import UserId


@dataclass
class MemberEntity(IEntity):
    id:UUID|None
    user_id:UserId
    group_id:'group.GroupId'
    point:float=0.0
    @classmethod
    def from_model(cls, data: "models.GroupUser") -> 'MemberEntity':
        return cls(
            id=data.id,
            user_id=data.user_id,
            group_id=data.group_id,
            point=data.point
        )
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'group_id': self.group_id,
            'point': self.point
        }