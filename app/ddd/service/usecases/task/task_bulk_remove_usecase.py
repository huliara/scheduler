from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import GroupId
from app.ddd.domain.task import ITaskRepository, TaskId


class TaskBulkRemoveUseCase(TransactionUseCaseBase):
    def __init__(self, db, task_repository: ITaskRepository):
        super().__init__(db)
        self.task_repository = task_repository
        
    def execute(self,group_id:GroupId,expired:bool|None, task_ids: list[TaskId]):
        return self._transaction(group_id,expired,task_ids)
    
    def _transaction(self,group_id,expired, task_ids: list[TaskId]):
        if expired:
            tasks = self.task_repository.find_all(group_id,end=True)
            return tasks
        tasks = self.task_repository.find_by_ids(group_id,task_ids)
        self.task_repository.bulk_remove(tasks)
        return tasks