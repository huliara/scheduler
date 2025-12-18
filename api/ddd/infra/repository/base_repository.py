from sqlalchemy.orm import Session
from models.models import User
from ddd.core.exception import DomainException
from ddd.core.i_entity import IEntity
from sqlalchemy.future import select

class SQLAlchemyBaseRepository[E:IEntity]():
    def __init__(self, db:Session):
        self.db = db
        self.Model=None
        self.Entity=None
        
    def find_by_id(self, id)->E:
        model=self.db.get(self.Model,id)
        return self._refresh_to_entity(model)
    
    def find_by_user(self, user_id)->list[E]:
        user=self.db.get(User,user_id)
        if user is None:
            raise DomainException('User not found',404)
        joining_group_ids=[group.group_id for group in user.groups]
        targets=self.db.scalars(select(self.Model).filter(self.Model.group_id.in_(joining_group_ids))).all()  
        return [self._refresh_to_entity(target) for target in targets]
    
    def find_by_group(self, group_id)->list[E]:
        models=self.db.scalars(select(self.Model).filter(self.Model.group_id==group_id)).all()
        return [self._refresh_to_entity(model) for model in models]
    
    def find_all(self)->list[E]:
        return [self._refresh_to_entity(model) for model in self.db.scalars(select(self.Model)).all()]
    
    def remove(self, id)->E:
        model=self.db.get(self.Model,id)
        resposnse=self._refresh_to_entity(model)
        if model is None:
            raise DomainException(f'{self.Model.__class__.__name__}:{id} not found',404)
        self.db.delete(model)
        self.db.commit()
        return resposnse
    
    def _refresh_to_entity(self, model)->E:
        entity=self.Entity.from_model(model)
        return entity