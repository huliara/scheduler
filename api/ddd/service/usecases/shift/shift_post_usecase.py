import datetime

from ddd.core.exception import UseCaseException
from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.group import IGroupRepository
from ddd.domain.shift import IShiftRepository, ShiftEntity
from ddd.domain.task import ITaskRepository, TaskId
from ddd.domain.user import IUserRepository, UserId


class ShiftPostUseCase(TransactionUseCaseBase):
    def __init__(self,
                 shift_repository:IShiftRepository,
                 user_repository:IUserRepository,
                 group_repository:IGroupRepository,
                 task_repository:ITaskRepository
                 ):
        self.shift_repository=shift_repository
        self.user_repository=user_repository
        self.group_repository=group_repository
        self.task_repository=task_repository   
        
    def execute(self,name:str,start_time:datetime.datetime,creater_id:UserId,task_id:TaskId)->ShiftEntity:
        return self._transaction(name,start_time,creater_id,task_id)
    
    def _transaction(self,name,start_time,creater_id,task_id)->ShiftEntity:
        try:
            _=self.user_repository.find_by_id(creater_id)
        except:
            raise UseCaseException(f'creater_id:{creater_id} not found')
        try:
            _=self.task_repository.find_by_id(task_id)
        except:
            raise UseCaseException(f'task_id:{task_id} not found')
        
        result=self.shift_repository.add(name,start_time,creater_id,task_id)
        return result