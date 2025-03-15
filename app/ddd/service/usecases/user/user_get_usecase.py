from app.ddd.domain.user import IUserRepository, UserEntity, UserId

from ..get_usecase import GetUseCase


class UserGetUsecase(GetUseCase[UserId,UserEntity,IUserRepository]):
    pass