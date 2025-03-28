from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import GroupId
from app.ddd.domain.task import ITaskRepository, TaskEntity


class TaskGetAllUseCase(TransactionUseCaseBase):
    def __init__(self,db,task_repository:ITaskRepository):
        super().__init__(db)
        self.task_repository=task_repository
    
    def execute(self,group_id:GroupId,end:bool|None)->list[TaskEntity]:
        return self._transaction(group_id,end)
    def _transaction(self,group_id,end)->list[TaskEntity]:
        result=self.task_repository.find_all(group_id,end)
        return result