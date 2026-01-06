from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.shift import IShiftRepository, ShiftId


class ShiftBulkRemoveUseCase(TransactionUseCaseBase):
    def __init__(self,  shift_repository: IShiftRepository):
        self.shift_repository = shift_repository
        
    def execute(self,shift_ids: list[ShiftId]):
        return self._transaction(shift_ids)
    
    def _transaction(self, shift_ids: list[ShiftId]):
        shifts = self.shift_repository.find_by_ids(shift_ids)
        self.shift_repository.bulk_remove(shifts)
        return shifts