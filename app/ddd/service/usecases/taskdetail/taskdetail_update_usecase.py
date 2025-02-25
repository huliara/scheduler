from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import IGroupRepository
from app.ddd.domain.task_detail import ITaskDetailRepository, TaskDetailEntity


class TaskDetailUpdateUseCase(TransactionUseCaseBase):
    def __init__(self, db,taskdetail_repository:ITaskDetailRepository,
                 group_repository:IGroupRepository):
        super().__init__(db)
        self.taskdetail_repository=taskdetail_repository
        self.group_repository=group_repository
    def execute(self, task_detail:TaskDetailEntity):
        
        return self._transaction(task_detail)
    
    def _transaction(self, task_detail:TaskDetailEntity):
        try:
            _=self.group_repository.find_by_id(task_detail.group_id)
        except:
            raise UseCaseException(f'group_id:{task_detail.group_id} not found')
        try:
            _=self.taskdetail_repository.find_by_id(task_detail.id)
        except:
            raise UseCaseException(f'taskdetail_id:{task_detail.id} not found')
        task_detail=self.taskdetail_repository.update(task_detail)
        return task_detail