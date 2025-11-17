from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import IGroupRepository
from app.ddd.domain.task import ITaskRepository, TaskEntity
from app.ddd.domain.user import IUserRepository


class UserRelateTaskDetailUseCase(TransactionUseCaseBase):
    def __init__(self, db, user_repository:IUserRepository,
                 taskdetail_repository:ITaskRepository,
                 group_repository:IGroupRepository):
        super().__init__(db)
        self.user_repository = user_repository
        self.taskdetail_repository = taskdetail_repository
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
        
        taskdetails=[]
        for group in groups:
            taskdetails+=self.taskdetail_repository.find_all(group['id'])
        
        return taskdetails