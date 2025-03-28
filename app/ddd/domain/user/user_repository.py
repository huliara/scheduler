from abc import abstractmethod

import app.ddd.domain.group as group
from app.ddd.core.i_repository import IRepository
from app.ddd.domain.user.user_entity import UserEntity, UserId
from app.models.models import User


class IUserRepository(IRepository[UserEntity,UserId]):
    @abstractmethod
    def find_all(self,group_id:'group.GroupId|None') -> list[UserEntity]:
        pass
    @abstractmethod
    def add(self,password:str, entity: UserEntity) -> UserEntity:
        pass
    
    @abstractmethod
    def _refresh_to_entity(self, model: User) -> UserEntity:
        pass
    
    @abstractmethod
    def update_password(self, user_id: UserId, password: str):
        pass
    
    
    
