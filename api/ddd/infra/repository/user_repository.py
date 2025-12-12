from ddd.core.exception import DomainException
from ddd.domain.user import IUserRepository, UserEntity
from ddd.infra.auth import get_password_hash
from ddd.infra.repository import SQLAlchemyBaseRepository
from models.models import GroupUser, Task, User
from sqlalchemy.future import select


class UserRepository(IUserRepository):
    def __init__(self, db):
        self.db = db

    def find_by_id(self, id):
        model = self.db.get(User, id)
        return self._refresh_to_entity(model)
    
    def find_by_ids(self, ids):
        models = self.db.scalars(select(User).filter(User.id.in_(ids))).all()
        return [self._refresh_to_entity(model) for model in models]
        
    def find_all(self,group_id):
        if group_id is not None:
            return [self._refresh_to_entity(model) for model in self.db.scalars(select(User)).join(GroupUser).filter(GroupUser.group_id==group_id).all()]
        return [self._refresh_to_entity(model) for model in self.db.scalars(select(User)).all()]
    
    def add(self, entity:UserEntity, password:str)->UserEntity:
        exp_tasks = self.db.scalars(select(Task).filter(Task.id.in_([task for task in entity.exp_tasks]))).all()
        model = User(
            name=entity.name,
            password=get_password_hash(password),
            room_number=entity.room_number,
            exp_tasks=exp_tasks,
            is_admin=entity.is_admin
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._refresh_to_entity(model)
    
    def update_password(self, user_id, password):
        target=self.db.get(User,user_id)
        if target is None:
            raise DomainException('User not found',404)
        target.password=get_password_hash(password)
        self.db.commit()    
        return
    
    def save(self, entity:UserEntity):
        model = self.db.get(User, entity.id)
        if model is None:
            raise DomainException('User not found',404)
        model.name = entity.name
        model.room_number = entity.room_number
        model.exp_tasks = self.db.scalars(select(Task).filter(Task.id.in_(entity.exp_tasks))).all()
        self.db.commit()
        self.db.refresh(model)
        return self._refresh_to_entity(model)
    
    def remove(self, id):
        model = self.db.get(User, id)
        if model is None:
            raise DomainException('User not found',404)
        self.db.delete(model)
        self.db.commit()
        return self._refresh_to_entity(model)
    
    def _refresh_to_entity(self, model)-> UserEntity:
        entity = UserEntity.from_model(model)
        return entity