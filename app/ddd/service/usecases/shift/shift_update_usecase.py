from sqlalchemy.orm import Session

from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.shift import IShiftRepository, Shift, ShiftId
from app.ddd.domain.task import ITaskRepository
from app.schemas.task import TaskCreate


class ShiftUpdateUseCase(TransactionUseCaseBase):
    def __init__(self,db:Session,
                 shift_repository:IShiftRepository,
                 task_repository:ITaskRepository
                 ):
        super().__init__(db)
        self.shift_repository=shift_repository
        self.task_repository=task_repository
        
    def execute(self,shift_id:ShiftId, request:TaskCreate)->Shift:
        return self._transaction(shift_id,request)
    def _transaction(self,shift_id:ShiftId,request:TaskCreate)->Shift:
        try:
            target_shift=self.shift_repository.find_by_id(shift_id)
        except:
            raise UseCaseException(f'task_id:{shift_id} not found')
        try:
            task=self.task_repository.find_by_id(request.task_id)
        except:
            raise UseCaseException(f'task_id:{request.task_id} not found')
        target_shift.name=request.name
        target_shift.start_time=request.start_time
        target_shift.task=task
        shift_new=self.shift_repository.save(target_shift)
        
        return shift_new