from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import GroupId
from app.ddd.domain.shift import IShiftRepository, ShiftId


class ShiftBulkRemoveUseCase(TransactionUseCaseBase):
    def __init__(self,  shift_repository: IShiftRepository):
        self.shift_repository = shift_repository
        
    def execute(self,group_id:GroupId,expired:bool|None, shift_ids: list[ShiftId]):
        return self._transaction(group_id,expired,shift_ids)
    
    def _transaction(self,group_id,expired, shift_ids: list[ShiftId]):
        if expired:
            shifts = self.shift_repository.find_all(group_id,end=True)
            return shifts
        shifts = self.shift_repository.find_by_ids(shift_ids)
        self.shift_repository.bulk_remove(shifts)
        return shifts