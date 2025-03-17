from sqlalchemy.future import select

from app.cruds.auth import get_password_hash
from app.ddd.core.exception import DomainException
from app.ddd.domain.user import IUserRepository, UserEntity
from app.models.models import TaskDetail, User


class UserRepository(IUserRepository):
    def __init__(self, db):
        self.db = db

    def find_by_id(self, id):
        model = self.db.get(User, id)
        return self._refresh_to_entity(model)
        
    def find_all(self):
        return [self._refresh_to_entity(model) for model in self.db.scalars(select(User)).all()]
    
    def add(self,password:str, entity:UserEntity):
        exp_tasks = self.db.scalars(select(TaskDetail).filter(TaskDetail.id.in_([task.id for task in entity.exp_tasks]))).all()
        model = User(
            name=entity.name,
            password=get_password_hash(password),
            room_number=entity.room_number,
            exp_tasks=exp_tasks,
        )
        self.db.add(model)
        self.db.commit()
        return self._refresh_to_entity(model)
    
    def save(self, entity:UserEntity):
        model = self.db.get(User, entity.id)
        if model is None:
            raise DomainException('User not found',404)
        model.name = entity.name
        model.room_number = entity.room_number
        model.exp_tasks = self.db.scalars(select(TaskDetail).filter(TaskDetail.id.in_([task.id for task in entity.exp_tasks]))).all()
        self.db.commit()
        return self._refresh_to_entity(model)
    
    def delete(self, id):
        model = self.db.get(User, id)
        if model is None:
            raise DomainException('User not found',404)
        self.db.delete(model)
        self.db.commit()
        return self._refresh_to_entity(model)
    
    def _refresh_to_entity(self, model):
        entity = UserEntity.from_model(model)
        return entity