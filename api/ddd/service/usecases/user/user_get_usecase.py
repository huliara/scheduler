from ddd.domain.user.user_entity import UserEntity
from ddd.domain.user.user_value_object import UserId
from ddd.domain.user.user_repository import IUserRepository

from ..get_usecase import GetUseCase


class UserGetUseCase(GetUseCase[UserId,UserEntity,IUserRepository]):
    pass