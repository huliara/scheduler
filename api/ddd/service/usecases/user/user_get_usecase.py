from ddd.domain.user import IUserRepository, UserEntity, UserId

from ..get_usecase import GetUseCase


class UserGetUseCase(GetUseCase[UserId,UserEntity,IUserRepository]):
    pass