from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import GroupId, IGroupRepository
from app.ddd.domain.task import ITaskRepository, TaskEntity, TaskId
from app.ddd.domain.user import IUserRepository, UserId


class TaskCompleteUseCase(TransactionUseCaseBase):
    def __init__(self, db,task_repository:ITaskRepository,user_repository:IUserRepository,group_repository:IGroupRepository):
        super().__init__(db)
        self.task_repository=task_repository
        self.user_repository=user_repository
        self.group_repository=group_repository 
        
    def execute(self,group_id:GroupId,task_id:TaskId,user_id:UserId)->TaskEntity:
        return self._transaction(group_id,task_id,user_id)
    
    def _transaction(self,group_id, task_id,user_id)->TaskEntity:
        try:
            group=self.group_repository.find_by_id(group_id)
        except:
            raise UseCaseException(f'group_id:{group_id} not found')
        try:
            target_task=self.task_repository.find_by_id(task_id)
        except:
            raise UseCaseException(f'task_id:{task_id} not found')
        try:
            user=self.user_repository.find_by_id(user_id)
        except:
            raise UseCaseException(f'user_id:{user_id} not found')
        
        task=target_task.complete(user)
        for worker in task.workers:
            try:
                member=group.get_member(worker.id)
            except:
                raise UseCaseException(f'user_id:{worker.id} not found in group_id:{group_id}')
            member.point+=task.taskdetail.wage
        
        self.group_repository.save(group)
        
        new_task=self.task_repository.save(task)
        return new_task