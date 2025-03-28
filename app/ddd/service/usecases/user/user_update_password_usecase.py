from dataclasses import dataclass

from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.user import IUserRepository, UserEntity, UserId


class UserUpdatePasswordUseCase(TransactionUseCaseBase):
    def __init__(self, db,user_repository:IUserRepository):
        super().__init__(db)
        self.user_repository=user_repository
    
    def execute(self,id:UserId,password:str):
        return super().execute(id,password)

    def _transaction(self,id,password):
        try:
            self.user_repository.update_password(id,password)
        except:
            raise UseCaseException('password update failed')
        return 