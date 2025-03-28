from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.ddd.core.i_entity import IEntity


class IRepository[T:IEntity,ID](ABC):
    
    @abstractmethod
    def __init__(self, db: Session) -> None:
        self.db=db
    
    @abstractmethod
    def find_by_id(self, id: ID) -> T:
        pass
    
    @abstractmethod
    def find_all(self,group_id) -> list[T]:
        pass
    
    @abstractmethod
    def add(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def save(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def remove(self, id: ID) -> T:
        pass
    
    