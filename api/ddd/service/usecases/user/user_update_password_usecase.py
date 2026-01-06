
from ddd.core.exception import UseCaseException
from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.user.user_value_object import UserId
from ddd.domain.user.user_repository import IUserRepository


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