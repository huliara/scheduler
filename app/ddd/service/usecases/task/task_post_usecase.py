import datetime

from sqlalchemy.orm import Session

from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import IGroupRepository
from app.ddd.domain.task import ITaskRepository, TaskEntity
from app.ddd.domain.task_detail import ITaskDetailRepository, TaskDetailId
from app.ddd.domain.user import IUserRepository, UserId


class TaskPostUseCase(TransactionUseCaseBase):
    def __init__(self,db:Session,
                 task_repository:ITaskRepository,
                 user_repository:IUserRepository,
                 group_repository:IGroupRepository,
                 taskdetail_repository:ITaskDetailRepository
                 ):
        super().__init__(db)
        self.task_repository=task_repository
        self.user_repository=user_repository
        self.group_repository=group_repository
        self.taskdetail_repository=taskdetail_repository   
        
    def execute(self,name:str,start_time:datetime.datetime,creater_id:UserId,taskdetail_id:TaskDetailId)->TaskEntity:
        return self._transaction(name,start_time,creater_id,taskdetail_id)
    
    def _transaction(self,name,start_time,creater_id,taskdetail_id)->TaskEntity:
        try:
            _=self.user_repository.find_by_id(creater_id)
        except:
            raise UseCaseException('creater_id:f{task.creater_id} not found')
        try:
            _=self.taskdetail_repository.find_by_id(taskdetail_id)
        except:
            raise UseCaseException('taskdetail_id:f{task.taskdetail_id} not found')
        
        result=self.task_repository.add(name,start_time,creater_id,taskdetail_id)
        return result