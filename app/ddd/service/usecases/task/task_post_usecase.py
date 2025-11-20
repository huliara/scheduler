from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import IGroupRepository
from app.ddd.domain.task import ITaskRepository, TaskEntity


class TaskPostUseCase(TransactionUseCaseBase):
    def __init__(self, task_repository:ITaskRepository,
                 group_repository:IGroupRepository):
        self.task_repository=task_repository
        self.group_repository=group_repository
    def execute(self, task:TaskEntity):
        
        return self._transaction(task)
    
    def _transaction(self, task:TaskEntity):
        try:
            _=self.group_repository.find_by_id(task.group_id)
        except:
            raise UseCaseException(f'group_id:{task.group_id} not found')
        task=self.task_repository.add(task)
        return task