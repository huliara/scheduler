from app.ddd.domain.user import IUserRepository, UserEntity, UserId

from ..remove_usecase import RemoveUseCase


class UserRemoveUseCase(RemoveUseCase[UserId,UserEntity,IUserRepository]):
    pass