
from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.group import IGroupRepository
from ddd.domain.shift import IShiftRepository, ShiftId
from ddd.domain.user.user_repository import IUserRepository

from .shifts_allocate_worker import (AllocWorkerDTO,
                                     ShiftAllocationWorkerUseCase)


class ShiftAllocationByGroup(TransactionUseCaseBase):
    def __init__(self,shift_repository:IShiftRepository,user_repository:IUserRepository,group_repository:IGroupRepository):
        self.shift_repository=shift_repository
        self.group_repository=group_repository
        self.user_repository=user_repository
    
    async def execute(self, shift_ids:list[ShiftId],group_id):
        
        shifts,users=self._transaction(shift_ids,group_id)
        results=await ShiftAllocationWorkerUseCase(self.user_repository,self.shift_repository).execute(shifts,users)
        return results
    
    def _transaction(self, shift_ids:list[ShiftId],group_id):
        shifts=self.shift_repository.find_by_ids(shift_ids)
        members=[member for member in self.group_repository.get_all_members(group_id)]
        users_dto=[]
        for member in members:
            user_dto=AllocWorkerDTO(
                id=member.user_id,
                point=member.point,
                exp_tasks=member.exp_tasks
            )
            users_dto.append(user_dto)
            
        return shifts,users_dto