from abc import ABC, abstractmethod
from ddd.core.i_entity import IEntity

class IRepository[T:IEntity,ID](ABC):
    
    @abstractmethod
    def __init__(self, db) -> None:
        pass
    
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
    
    @abstractmethod
    def _refresh_to_entity(self, model) -> T:
        pass
    