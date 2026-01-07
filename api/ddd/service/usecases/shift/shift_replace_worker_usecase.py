from ddd.core.exception import UseCaseException
from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.group import IGroupRepository
from ddd.domain.member import IMemberRepository
from ddd.domain.shift import IShiftRepository, ShiftEntity, ShiftId
from ddd.domain.user.user_value_object import  UserId
from ddd.domain.user.user_repository import IUserRepository
import datetime

class ShiftReplaceWorkerUseCase(TransactionUseCaseBase):
    def __init__(self,
                 shift_repository:IShiftRepository,
                 user_repository:IUserRepository,
                 group_repository:IGroupRepository,
                 member_repository:IMemberRepository):
        self.shift_repository=shift_repository
        self.user_repository=user_repository
        self.group_repository=group_repository 
        self.member_repository=member_repository
        
    def execute(self,shift_id:ShiftId,old_user_id:UserId,new_user_id:UserId)->ShiftEntity:
        return self._transaction(shift_id,old_user_id,new_user_id)
    
    def _transaction(self, shift_id,old_user_id,new_user_id)->ShiftEntity:
        try:
            target_shift=self.shift_repository.find_by_id(shift_id)
        except:
            raise UseCaseException(f'shift_id:{shift_id} not found')
        try:
            old_user=self.user_repository.find_by_id(old_user_id)
        except:
            raise UseCaseException(f'user_id:{old_user_id} not found')
        try:
            new_user=self.user_repository.find_by_id(new_user_id)
        except:
            raise UseCaseException(f'user_id:{new_user_id} not found')
        
        
        
        shift=target_shift.replace_worker(old_user,new_user)
        
        if shift.end_time<datetime.datetime.now():
            shift=shift.complete(new_user)
            try:
                member=self.member_repository.find_by_id(shift.task.group_id,new_user.id)
            except:
                raise UseCaseException(f'user_id:{new_user.id} not found in group_id:{shift.task.group_id}')
            member.point+=shift.task.wage
            new_user.add_exp(shift.task.id)
            _=self.member_repository.save(member)
            _=self.user_repository.save(new_user)
       
        new_shift=self.shift_repository.save(shift)
        return new_shift