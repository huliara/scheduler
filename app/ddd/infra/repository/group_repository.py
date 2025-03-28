from sqlalchemy.future import select

from app.ddd.core.exception import DomainException
from app.ddd.domain.group import (GroupEntity, GroupId, IGroupRepository,
                                  MemberEntity)
from app.models.models import Group, GroupUser


class GroupRepository(IGroupRepository):
    def __init__(self, db):
        super().__init__(db)
    
    def find_by_id(self, id):
        model=self.db.get(Group,id)
        return self._refresh_to_entity(model)
    
    def find_all(self):
        return [self._refresh_to_entity(model) 
                for model in self.db.scalars(select(Group)).all()]
    
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
        model.users=[ GroupUser(group_id=model.id,user_id=user.user.id,point=user.point) for user in entity.users]
        self.db.commit()
        self.db.refresh(model)
        return self._refresh_to_entity(model)
    
    def remove(self, id):
        model=self.db.get(Group,id)
        if model is None:
            raise DomainException('Group not found',404)
        self.db.delete(model)
        self.db.commit()
        return self._refresh_to_entity(model)
    
        
    def _refresh_to_entity(self, model: Group) -> GroupEntity:
        return GroupEntity.from_model(model)
    
    def get_all_members(self, id: GroupId) -> list[MemberEntity]:
        group=self.db.get(Group,id)
        return [MemberEntity.from_model(user) for user in group.users ]
    