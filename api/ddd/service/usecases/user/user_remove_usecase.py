from ddd.domain.user.user_entity import UserEntity
from ddd.domain.user.user_value_object import UserId
from ddd.domain.user.user_repository import IUserRepository

from ..remove_usecase import RemoveUseCase


class UserRemoveUseCase(RemoveUseCase[UserId,UserEntity,IUserRepository]):
    pass