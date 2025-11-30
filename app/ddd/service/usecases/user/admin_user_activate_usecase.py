from ddd.core.exception import UseCaseException
from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.user import IUserRepository, UserEntity


class AdminUserActivateUseCase(TransactionUseCaseBase):
    def __init__(self,user_repository:IUserRepository):
        self.user_repository=user_repository
    
    def execute(self,user_id:str,activate:bool)->UserEntity:
        return super().execute(user_id,activate)
    
    def _transaction(self, user_id:str,activate:bool)->UserEntity:
        try:
            target_user=self.user_repository.find_by_id(user_id)
        except:
            raise UseCaseException(f'user_id:{user_id} not found')
        
        target_user.is_active=activate
        try:
            user=self.user_repository.save(target_user)
        except:
            raise UseCaseException(f'invalid enitity:{target_user}')
        return user