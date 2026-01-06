from ddd.domain.user.user_entity import UserEntity

from ddd.domain.user.user_repository import IUserRepository

from ..getall_usecase import GetAllUseCase


class UserGetAllUseCase(GetAllUseCase[UserEntity,IUserRepository]):
    pass