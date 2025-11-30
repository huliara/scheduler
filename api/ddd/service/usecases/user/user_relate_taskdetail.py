from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.group import IGroupRepository
from ddd.domain.task import ITaskRepository, TaskEntity
from ddd.domain.user import IUserRepository


class UserRelateTaskUseCase(TransactionUseCaseBase):
    def __init__(self, user_repository:IUserRepository,
                 task_repository:ITaskRepository,
                 group_repository:IGroupRepository):
        self.user_repository = user_repository
        self.task_repository = task_repository
        self.group_repository = group_repository

    def execute(self, user_id)->list[TaskEntity]:
        return self._transaction(user_id)
    
    def _transaction(self, user_id):
        try:
            user = self.user_repository.find_by_id(user_id)
        except:
            raise Exception(f'User:ID{user_id} not found')
        try:
            groups = self.group_repository.find_by_user_id(user.id)
        except:
            raise Exception(f'There are invalid groups')
        
        task=[]
        for group in groups:
            task+=self.task_repository.find_all(group['id'])
        
        return task