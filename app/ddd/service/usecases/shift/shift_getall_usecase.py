from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import GroupId
from app.ddd.domain.shift import IShiftRepository, Shift


class ShiftGetAllUseCase(TransactionUseCaseBase):
    def __init__(self,db,shift_repository:IShiftRepository):
        super().__init__(db)
        self.shift_repository=shift_repository
    
    def execute(self,group_id:GroupId,end:bool|None)->list[Shift]:
        return self._transaction(group_id,end)
    def _transaction(self,group_id,end)->list[Shift]:
        result=self.shift_repository.find_all(group_id,end)
        return result