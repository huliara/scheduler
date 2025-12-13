from ddd.core.exception import DomainException
from ddd.domain.group import GroupId
from ddd.domain.member import IMemberRepository, MemberEntity
from ddd.domain.user import UserId
from ddd.infra.repository import SQLAlchemyBaseRepository
from models.models import Group, GroupUser, User
from sqlalchemy import insert
from sqlalchemy.future import select


class MemberRepository(SQLAlchemyBaseRepository,IMemberRepository):
    
    def find_by_id(self, group_id:GroupId, user_id:UserId):
        member=self.db.scalars(select(GroupUser).filter_by(group_id=group_id, user_id=user_id)).first()
        if member is None:
            return None
        return self._refresh_to_entity(member)
    
    def find_by_group_id(self, group_id:GroupId):
        members=self.db.scalars(select(GroupUser).filter_by(group_id=group_id)).all()
        return [{
            'id':member.user_id,
            'name':member.user.name,
            'room_number':member.user.room_number,
            'point':member.point,
            'is_active':member.user.is_active,
        }
            for member in members]

    def find_all(self, group_id:GroupId, room_number):
        if room_number is None:
            members=self.db.scalars(select(GroupUser).filter_by(group_id=group_id)).all()
        else:
            members=self.db.scalars(select(GroupUser).join(User).
                                    filter(GroupUser.group_id==group_id,User.room_number.like(f"%{room_number}%"))).all()
        return [self._refresh_to_entity(member) for member in members]

    def add(self, entity:MemberEntity):
        request=self.db.get(GroupUser, (entity.group_id, entity.user_id))
        if request is not None:
            raise DomainException(f'member_id:{entity.user_id} is already in group_id:{entity.group_id}')
        model=GroupUser(
            group_id=entity.group_id,
            user_id=entity.user_id,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._refresh_to_entity(model)

    def bulk_add(self,group_id, entities:list[MemberEntity]):
        group=self.db.get(Group,group_id)
        if group is None:
            raise DomainException(f'group_id:{group_id} not found')
        target=self.db.scalars(select(GroupUser).filter(GroupUser.group_id==group_id,
                                                         GroupUser.user_id.in_([entity.user_id for entity in entities]))).all()
        if len(target)>0:
            raise DomainException(f'member_id is already in group_id')
        data=[entity.to_dict() for entity in entities]
        result=self.db.scalars(insert(GroupUser).returning(GroupUser),data).all()
        self.db.commit()
        for model in result:
            self.db.refresh(model)
        return [self._refresh_to_entity(model) for model in result]

    def save(self, entity):
        model=self.db.get(GroupUser,(entity.group_id,entity.user_id))
        if model is None:
            raise DomainException(f'member_id:{entity.user_id} is not found in group_id:{entity.group_id}')
        model.point=entity.point
        self.db.commit()
        self.db.refresh(model)
        return self._refresh_to_entity(model)

    def remove(self, user_id, group_id):
        model=self.db.get(GroupUser,(group_id,user_id))
        if model is None:
            raise DomainException(f'member_id:{user_id} is not found in group_id:{group_id}')
        self.db.delete(model)
        self.db.commit()
        return self._refresh_to_entity(model)
        
    
    def _refresh_to_entity(self, model:GroupUser)->MemberEntity:
        entity=MemberEntity.from_model(model)
        return entity
        