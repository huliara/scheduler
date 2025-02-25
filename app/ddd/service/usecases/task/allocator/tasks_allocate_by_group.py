from sqlalchemy.orm import Session

from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import GroupId
from app.ddd.domain.task import ITaskRepository, TaskEntity, TaskId
from app.ddd.domain.user import IUserRepository, UserEntity, UserId

from .tasks_allocate_worker import TasksAllocationWorkerUseCase


class TaskAllocationByGroup(TransactionUseCaseBase):
    def __init__(self,db:Session,task_repository:ITaskRepository,user_repository:IUserRepository):
        super().__init__(db)
        self.task_repository=task_repository
        self.user_repository=user_repository
    
    async def execute(self, task_ids:list[TaskId],group_id:GroupId):
        
        tasks,users=self._transaction(task_ids,group_id)
        results=await TasksAllocationWorkerUseCase(self.db).shift_calculate(users,tasks)
        
        return results
    
    def _transaction(self, task_ids:list[TaskId], group_id:GroupId):
        tasks=self.task_repository.find_by_id(task_ids)
        users=self.user_repository.find_by_group_id(group_id)
        
        return tasks,users