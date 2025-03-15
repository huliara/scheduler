from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.user import IUserRepository, UserEntity


class UserPostUseCase(TransactionUseCaseBase):
    def __init__(self, db,user_repository:IUserRepository):
        super().__init__(db)
        self.user_repository=user_repository
    
    def execute(self,user_entity:UserEntity):
        return super().execute(user_entity)
    
    def _transaction(self, user_entity:UserEntity):
        try:
            user=self.user_repository.add(user_entity)
        except:
            raise UseCaseException(f'user_id:{user_entity.id} not found')
        return user