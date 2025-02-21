from abc import abstractmethod

from sqlalchemy.orm import Session

from app.ddd.core.i_repository import IRepository
from app.ddd.domain.user.user_entity import UserEntity, UserId
from app.models.models import User


class IUserRepository(IRepository[UserEntity,UserId]):
    
    @abstractmethod
    def refresh_to_entity(self, model: User) -> UserEntity:
        pass