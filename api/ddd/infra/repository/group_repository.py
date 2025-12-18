from ddd.core.exception import DomainException
from ddd.domain.group import (GroupEntity, GroupId, IGroupRepository,
                              MemberEntity)
from models.models import Group, GroupUser

from .base_repository import SQLAlchemyBaseRepository


class GroupRepository(SQLAlchemyBaseRepository[GroupEntity],IGroupRepository):
    def __init__(self, db):
        super().__init__(db)
        self.Model=Group
        self.Entity=GroupEntity
    
    def find_by_group(self, group_id):
        return self.find_by_id(group_id)
    
    def add(self, entity):
        model=Group(
            name=entity.name,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._refresh_to_entity(model)
    
    def save(self, entity:GroupEntity):
        model=self.db.get(Group,entity.id)
        if model is None:
            raise DomainException('Group not found',404)
        model.name=entity.name
        model.users=[ GroupUser(group_id=model.id,user_id=user.user_id,point=user.point) for user in entity.users]
        self.db.commit()
        self.db.refresh(model)
        return self._refresh_to_entity(model)
    
    
    def get_all_members(self, id: GroupId) -> list[MemberEntity]:
        group=self.db.get(Group,id)
        return [MemberEntity.from_model(user) for user in group.users ]
    