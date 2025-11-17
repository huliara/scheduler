from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import IGroupRepository
from app.ddd.domain.task import ITaskRepository, TaskEntity


class TaskDetailPostUseCase(TransactionUseCaseBase):
    def __init__(self, db,taskdetail_repository:ITaskRepository,
                 group_repository:IGroupRepository):
        super().__init__(db)
        self.taskdetail_repository=taskdetail_repository
        self.group_repository=group_repository
    def execute(self, task_detail:TaskEntity):
        
        return self._transaction(task_detail)
    
    def _transaction(self, task_detail:TaskEntity):
        try:
            _=self.group_repository.find_by_id(task_detail.group_id)
        except:
            raise UseCaseException(f'group_id:{task_detail.group_id} not found')
        task_detail=self.taskdetail_repository.add(task_detail)
        return task_detail