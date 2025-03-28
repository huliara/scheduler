from sqlalchemy.orm import Session

from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import GroupId, IGroupRepository
from app.ddd.domain.task import ITaskRepository, TaskEntity, TaskId

from .tasks_allocate_worker import TaskAllocationWorkerUseCase


class TaskAllocationByGroup(TransactionUseCaseBase):
    def __init__(self,db:Session,task_repository:ITaskRepository,group_repository:IGroupRepository):
        super().__init__(db)
        self.task_repository=task_repository
        self.group_repository=group_repository
    
    async def execute(self, task_ids:list[TaskId],group_id:GroupId):
        
        tasks,users=self._transaction(task_ids,group_id)
        results=await TaskAllocationWorkerUseCase().shift_calculate(users,tasks)
        response=self.task_repository.bulk_update(results)
        return response
    
    def _transaction(self, task_ids:list[TaskId], group_id:GroupId):
        tasks=self.task_repository.find_by_id(task_ids)
        users=[member.user for member in self.group_repository.get_all_members(group_id)]
        
        return tasks,users