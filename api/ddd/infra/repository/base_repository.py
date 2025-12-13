from ddd.core.i_repository import IRepository
from models.models import Base
from ddd.core.i_entity import IEntity
from sqlalchemy.future import select
from sqlalchemy.orm import Session


class SQLAlchemyBaseRepository[T:Base,U:IEntity]():
    def __init__(self, db:Session):
        self.db = db
        
