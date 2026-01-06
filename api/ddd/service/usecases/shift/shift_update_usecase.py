
from ddd.core.exception import UseCaseException
from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.shift import IShiftRepository, ShiftEntity, ShiftId
from ddd.domain.task.task_repository import ITaskRepository
from schemas.shift import ShiftCreate


class ShiftUpdateUseCase(TransactionUseCaseBase):
    def __init__(self,
                 shift_repository:IShiftRepository,
                 task_repository:ITaskRepository
                 ):
        self.shift_repository=shift_repository
        self.task_repository=task_repository
        
    def execute(self,shift_id:ShiftId, request:ShiftCreate)->ShiftEntity:
        return self._transaction(shift_id,request)
    def _transaction(self,shift_id:ShiftId,request:ShiftCreate)->ShiftEntity:
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