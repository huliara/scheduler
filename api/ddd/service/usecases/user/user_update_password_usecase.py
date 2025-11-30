from dataclasses import dataclass

from ddd.core.exception import UseCaseException
from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.user import IUserRepository, UserEntity, UserId


class UserUpdatePasswordUseCase(TransactionUseCaseBase):
    def __init__(self, user_repository:IUserRepository):
        self.user_repository=user_repository
    
    def execute(self,id:UserId,password:str):
        return super().execute(id,password)

    def _transaction(self,id,password):
        try:
            self.user_repository.update_password(id,password)
        except:
            raise UseCaseException('password update failed')
        return 