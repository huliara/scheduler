from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.user import IUserRepository, UserEntity


class AdminUserAdminateUseCase(TransactionUseCaseBase):
    def __init__(self, user_repository:IUserRepository):
        self.user_repository=user_repository
    
    def execute(self,user_id:str,admin:bool)->UserEntity:
        return super().execute(user_id,admin)
    
    def _transaction(self, user_id:str,admin:bool)->UserEntity:
        try:
            target_user=self.user_repository.find_by_id(user_id)
        except:
            raise UseCaseException(f'user_id:{user_id} not found')
        
        target_user.is_admin=admin
        try:
            user=self.user_repository.save(target_user)
        except:
            raise UseCaseException(f'invalid enitity:{target_user}')
        return user