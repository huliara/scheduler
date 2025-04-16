from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

import app.ddd.domain.group as group
from app.ddd.domain.member import MemberEntity
from app.ddd.domain.user import UserId


class IMemberRepository(ABC):
    @abstractmethod
    def __init__(self, db:Session) -> None:
        self.db = db
        
    @abstractmethod 
    def find_by_id(self,group_id:'group.GroupId', user_id: UserId)->MemberEntity:
        pass
    
    @abstractmethod
    def find_by_group_id(self,group_id:'group.GroupId'):
        pass
    
    @abstractmethod
    def find_all(self,group_id:'group.GroupId',room_number:str|None)->list[MemberEntity]:
        pass
    
    @abstractmethod
    def add(self, entity: MemberEntity) -> MemberEntity:
        pass
    @abstractmethod
    def bulk_add(self, entities: list[MemberEntity]) -> list[MemberEntity]:
        pass
    @abstractmethod
    def save(self, entity:MemberEntity) -> MemberEntity:
        pass
    
    @abstractmethod
    def remove(self, user_id: UserId,group_id:'group.GroupId') -> MemberEntity:
        pass