from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import IGroupRepository
from app.ddd.domain.task import ITaskRepository
from app.ddd.domain.user import IUserRepository, UserId


class UserGetUseCase(TransactionUseCaseBase):
    def __init__(self,db,user_repository:IUserRepository,
                 taskdetail_repository:ITaskRepository,
                 group_repository:IGroupRepository):
        super().__init__(db)
        self.user_repository=user_repository
        self.taskdetail_repository=taskdetail_repository
        self.group_repository=group_repository
    def execute(self,user_id:UserId):
        return self._transaction(user_id)
    def _transaction(self,user_id:UserId):
        try:
            user=self.user_repository.find_by_id(user_id)
        except:
            raise Exception(f'User:ID{user_id} not found')
        try:
            taskdetails=self.taskdetail_repository.find_by_ids(user.exp_tasks)
        except:
            raise Exception(f'There are invalid Exp_task')
        try:
            groups=self.group_repository.find_by_user_id(user.id)
        except:
            raise Exception(f'There are invalid groups')
        return {
            'user':user,
            'taskdetails':taskdetails,
            'groups':groups
        }