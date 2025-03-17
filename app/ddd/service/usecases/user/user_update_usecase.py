from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.task_detail import ITaskDetailRepository
from app.ddd.domain.user import IUserRepository, UserEntity


class UserUpdateUseCase(TransactionUseCaseBase):
    def __init__(self, db,user_repository:IUserRepository,taskdetail_repository:ITaskDetailRepository):
        super().__init__(db)
        self.user_repository=user_repository
        self.taskdetail_repository=taskdetail_repository
    
    def execute(self,user_entity:UserEntity):
        return super().execute(user_entity)
    
    def _transaction(self, user_entity:UserEntity):
        try:
            _=self.taskdetail_repository.find_by_ids([taskdetail.id for taskdetail in user_entity.exp_tasks])
        except:
            raise UseCaseException('Invalid exp_task found')
        
        try:
            user=self.user_repository.save(user_entity)
        except:
            raise UseCaseException(f'user_id:{user_entity.id} not found')
        return user