from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.user import IUserRepository, UserEntity


class UserPostUseCase(TransactionUseCaseBase):
    def __init__(self,user_repository:IUserRepository):
        self.user_repository=user_repository
    
    def execute(self,entity:UserEntity,password:str)->UserEntity:
        return self._transaction(entity,password)
    
    def _transaction(self, entity:UserEntity,password:str)->UserEntity:
        try:
            user=self.user_repository.add(entity,password)
        except:
            raise UseCaseException(f'invalid enitity:{entity}')
        return user