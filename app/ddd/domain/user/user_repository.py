from abc import abstractmethod

import app.ddd.domain.group as group
import app.models.models as models
from app.ddd.core.i_repository import IRepository
from app.ddd.domain.user.user_entity import UserEntity, UserId


class IUserRepository(IRepository[UserEntity,UserId]):
    @abstractmethod
    def find_all(self,group_id:'group.GroupId|None') -> list[UserEntity]:
        pass
    @abstractmethod
    def add(self,password:str, entity: UserEntity) -> UserEntity:
        pass
    
    @abstractmethod
    def find_by_ids(self, ids: list[UserId]) -> list[UserEntity]:
        pass
    
    @abstractmethod
    def _refresh_to_entity(self, model: "models.User") -> UserEntity:
        pass
    
    @abstractmethod
    def update_password(self, user_id: UserId, password: str):
        pass
    
    
    
