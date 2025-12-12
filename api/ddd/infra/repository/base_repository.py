from ddd.core.i_repository import IRepository
from models.models import Base
from ddd.core.i_entity import IEntity
from sqlalchemy.future import select
from sqlalchemy.orm import Session


class SQLAlchemyBaseRepository[T:Base,U:IEntity]():
    def __init__(self, db:Session):
        self.db = db
        
    def find_by_id(self, id) -> T:
        model = self.db.get(T, id)
        return self._refresh_to_entity(model)
    
    def find_by_ids(self, ids) -> list[U]:
        models=self.db.scalars(select(T).filter(T.id.in_(ids))).all()
        return [self._refresh_to_entity(model) for model in models]
    
    def remove(self,id):
        model=self.db.get(T,id)
        if model is None:
            raise Exception(f'{T.__name__}:{id} not found')
        self.db.delete(model)
        self.db.commit()
        return self._refresh_to_entity(model)
    
    def _refresh_to_entity(self, model:T) -> U:
        entity= U.from_model(model)
        return entity