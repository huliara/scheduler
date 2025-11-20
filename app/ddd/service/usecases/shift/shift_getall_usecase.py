from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import GroupId
from app.ddd.domain.shift import IShiftRepository, ShiftEntity
from app.ddd.domain.user import UserEntity


class ShiftGetAllUseCase(TransactionUseCaseBase):
    def __init__(self,shift_repository:IShiftRepository):
        
        self.shift_repository=shift_repository
    
    def execute(self,user:UserEntity,group_id:GroupId|None,end:bool|None)->list[ShiftEntity]:
        return self._transaction(user,group_id,end)
    def _transaction(self,user,group_id,end)->list[ShiftEntity]:
        if group_id is None and not user.is_admin:
            raise Exception('group_id is required for non-admin users')
        result=self.shift_repository.find_all(group_id,end)
        return result