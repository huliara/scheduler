from ddd.core.exception import UseCaseException
from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.shift import IShiftRepository, ShiftEntity, ShiftId
from ddd.domain.user.user_value_object import  UserId
from ddd.domain.user.user_repository import IUserRepository

class ShiftAssignUseCase(TransactionUseCaseBase):
    def __init__(self, shift_repository:IShiftRepository,user_repository:IUserRepository):
        self.shift_repository=shift_repository
        self.user_repository=user_repository
        
    def execute(self,shift_id:ShiftId,user_id:UserId)->ShiftEntity:
        return self._transaction(shift_id,user_id)
    
    def _transaction(self, shift_id,user_id)->ShiftEntity:
        try:
            target_shift=self.shift_repository.find_by_id(shift_id)
        except:
            raise UseCaseException(f'shift_id:{shift_id} not found')
        try:
            user=self.user_repository.find_by_id(user_id)
        except:
            raise UseCaseException(f'user_id:{user_id} not found')
        shift=target_shift.add(user)
        new_shift=self.shift_repository.save(shift)
        return new_shift