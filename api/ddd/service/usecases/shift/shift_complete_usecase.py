from ddd.core.exception import UseCaseException
from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.group import IGroupRepository
from ddd.domain.member import IMemberRepository
from ddd.domain.shift import IShiftRepository, ShiftEntity, ShiftId, ShiftState
from ddd.domain.user import IUserRepository, UserId


class ShiftCompleteUseCase(TransactionUseCaseBase):
    def __init__(self, 
                 shift_repository:IShiftRepository,
                 user_repository:IUserRepository,
                 group_repository:IGroupRepository,
                 member_repository:IMemberRepository):
        self.shift_repository=shift_repository
        self.user_repository=user_repository
        self.group_repository=group_repository 
        self.member_repository=member_repository
        
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
        
        shift=target_shift.complete(user)
        member_list=[]
        user_list=[]
        group_id=shift.task.group_id
        for worker in shift.workers:
            try:
                member=self.member_repository.find_by_id(group_id,worker.id)
            except:
                raise UseCaseException(f'user_id:{worker.id} not found in group_id:{group_id}')
            member.point+=shift.task.wage
            user.add_exp(shift.task.id)
            member_list.append(member)
            user_list.append(worker)
       
        for member in member_list:
            _=self.member_repository.save(member)
            
        for user in user_list:
            _=self.user_repository.save(user)
        
        shift.status=ShiftState.archive
        new_shift=self.shift_repository.save(shift)
        return new_shift