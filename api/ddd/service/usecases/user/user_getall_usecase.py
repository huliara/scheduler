from ddd.domain.user import IUserRepository, UserEntity

from ..getall_usecase import GetAllUseCase


class UserGetAllUseCase(GetAllUseCase[UserEntity,IUserRepository]):
    pass