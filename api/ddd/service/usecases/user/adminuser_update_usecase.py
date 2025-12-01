from ddd.core.exception import UseCaseException
from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.user import IUserRepository, UserEntity


class AdminUserUpdateUseCase(TransactionUseCaseBase):
    def __init__(self, user_repository:IUserRepository):
        self.user_repository=user_repository
    
    def execute(self,user_entity:UserEntity):
        return super().execute(user_entity)
    
    def _transaction(self, user_entity:UserEntity):
        try:
            target_user=self.user_repository.find_by_id(user_entity.id)
        except:
            raise UseCaseException(f'user_id:{user_entity.id} not found')
        
        target_user.name=user_entity.name
        target_user.room_number=user_entity.room_number
        target_user.point=user_entity.point
        try:
            user=self.user_repository.save(target_user)
        except:
            raise UseCaseException(f'invalid enitity:{user_entity}')
        return user