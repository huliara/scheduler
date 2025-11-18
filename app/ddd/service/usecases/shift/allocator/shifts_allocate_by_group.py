from sqlalchemy.orm import Session

from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import GroupId, IGroupRepository
from app.ddd.domain.shift import IShiftRepository, Shift, ShiftId

from .shifts_allocate_worker import ShiftAllocationWorkerUseCase


class ShiftAllocationByGroup(TransactionUseCaseBase):
    def __init__(self,db:Session,shift_repository:IShiftRepository,group_repository:IGroupRepository):
        super().__init__(db)
        self.shift_repository=shift_repository
        self.group_repository=group_repository
    
    async def execute(self, shift_ids:list[ShiftId],group_id:GroupId):
        
        shifts,users=self._transaction(shift_ids,group_id)
        results=await ShiftAllocationWorkerUseCase().shift_calculate(users,shifts)
        response=self.shift_repository.bulk_update(results)
        return response
    
    def _transaction(self, shift_ids:list[ShiftId], group_id:GroupId):
        shifts=self.shift_repository.find_by_id(shift_ids)
        users=[member.user for member in self.group_repository.get_all_members(group_id)]
        
        return shifts,users