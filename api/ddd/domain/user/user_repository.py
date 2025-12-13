from abc import abstractmethod

import ddd.domain.group as group
from ddd.core.i_repository import IRepository
from ddd.domain.user.user_entity import UserEntity, UserId


class IUserRepository(IRepository[UserEntity,UserId]):
    @abstractmethod
    def find_all(self,group_id:'group.GroupId|None') -> list[UserEntity]:
        pass
    @abstractmethod
    def add(self,password:str, entity: UserEntity) -> UserEntity:
        pass
    @abstractmethod
    def update_password(self, user_id: UserId, password: str):
        pass
    
    
    
