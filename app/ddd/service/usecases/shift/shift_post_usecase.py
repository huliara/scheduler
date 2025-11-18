import datetime

from sqlalchemy.orm import Session

from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import IGroupRepository
from app.ddd.domain.shift import IShiftRepository, Shift
from app.ddd.domain.task import ITaskRepository, TaskId
from app.ddd.domain.user import IUserRepository, UserId


class ShiftPostUseCase(TransactionUseCaseBase):
    def __init__(self,db:Session,
                 shift_repository:IShiftRepository,
                 user_repository:IUserRepository,
                 group_repository:IGroupRepository,
                 task_repository:ITaskRepository
                 ):
        super().__init__(db)
        self.shift_repository=shift_repository
        self.user_repository=user_repository
        self.group_repository=group_repository
        self.task_repository=task_repository   
        
    def execute(self,name:str,start_time:datetime.datetime,creater_id:UserId,task_id:TaskId)->Shift:
        return self._transaction(name,start_time,creater_id,task_id)
    
    def _transaction(self,name,start_time,creater_id,task_id)->Shift:
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