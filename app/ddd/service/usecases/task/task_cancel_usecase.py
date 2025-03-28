from sqlalchemy.orm import Session

from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.task import ITaskRepository, TaskEntity, TaskId
from app.ddd.domain.user import IUserRepository, UserId


class TaskCancelUseCase(TransactionUseCaseBase):
    def __init__(self,db:Session,
                 task_repository:ITaskRepository,
                 user_repository:IUserRepository,
                 ):
        super().__init__(db)
        self.task_repository=task_repository
        self.user_repository=user_repository        
        
    def execute(self,task_id:TaskId, user_id:UserId)->TaskEntity:
        return self._transaction(task_id,user_id)
    def _transaction(self,task_id:TaskId,user_id:UserId)->TaskEntity:
        try:
            target_task=self.task_repository.find_by_id(task_id)
        except:
            raise UseCaseException('task_id:f{task_id} not found')
        try:
            worker=self.user_repository.find_by_id(user_id)
        except:
            raise UseCaseException('taskdetail_id:f{user_id} not found')
        target_task.remove(worker)
        task_new=self.task_repository.save(target_task)
    
        return task_new