from sqlalchemy.orm import Session

from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import IGroupRepository
from app.ddd.domain.task import ITaskRepository, TaskEntity
from app.ddd.domain.user import IUserRepository, UserId


class TaskPostUseCase(TransactionUseCaseBase):
    def __init__(self,db:Session,
                 task_repository:ITaskRepository,
                 user_repository:IUserRepository,
                 group_repository:IGroupRepository):
        super().__init__(db)
        self.task_repository=task_repository
        self.user_repository=user_repository
        self.group_repository=group_repository
        
    def execute(self,task:TaskEntity)->TaskEntity:
        return self._transaction(task)
    
    def _transaction(self,task:TaskEntity)->TaskEntity:
        try:
            _=self.user_repository.find_by_id(task.creater_id)
        except:
            raise UseCaseException('creater_id:f{task.creater_id} not found')
        try:
            _=self.group_repository.find_by_id(task.group_id)
        except:
            raise UseCaseException('group_id:f{task.group_id} not found')
        result=self.task_repository.add(task)
        return result