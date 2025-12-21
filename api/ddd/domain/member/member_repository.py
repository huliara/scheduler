from abc import ABC, abstractmethod

import ddd.domain.group as group
from ddd.domain.member import MemberEntity
from ddd.domain.user import UserId
from sqlalchemy.orm import Session


class IMemberRepository(ABC):
    @abstractmethod
    def __init__(self, db:Session) -> None:
        self.db = db
        
    @abstractmethod 
    def find_by_id(self,group_id:'group.GroupId', user_id: UserId)->MemberEntity:
        pass
    
    @abstractmethod
    def find_by_group(self,group_id:'group.GroupId'):
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