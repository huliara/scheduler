from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.shift import IShiftRepository
from ddd.domain.group import GroupId

class ShiftRemoveOrphanUseCase(TransactionUseCaseBase):
    def __init__(self,  shift_repository: IShiftRepository):
        self.shift_repository = shift_repository
        
    def execute(self,group_id:GroupId ):
        return self._transaction(group_id)
    
    def _transaction(self, group_id:GroupId):
        shifts = self.shift_repository.find_by_group(group_id)
        shifts= [shift for shift in shifts if shift.is_orphan]
        self.shift_repository.bulk_remove(shifts)
        return shifts