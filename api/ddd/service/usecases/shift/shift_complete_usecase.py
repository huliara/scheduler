from ddd.core.exception import UseCaseException
from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.group import IGroupRepository
from ddd.domain.member import IMemberRepository
from ddd.domain.shift import IShiftRepository, ShiftEntity, ShiftId
from ddd.domain.user.user_repository import IUserRepository
from ddd.domain.user.user_value_object import UserId
from env import KUMANO_LOCATION, ACCEPTABLE_LOCATION_ERROR
import datetime


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
        
    def execute(self,shift_id:ShiftId,user_id:UserId,location:tuple[float,float])->ShiftEntity:
        return self._transaction(shift_id,user_id,location)
    
    def _transaction(self, shift_id,user_id,location)->ShiftEntity:
        try:
            target_shift=self.shift_repository.find_by_id(shift_id)
        except:
            raise UseCaseException(f'shift_id:{shift_id} not found')
        try:
            user=self.user_repository.find_by_id(user_id)
        except:
            raise UseCaseException(f'user_id:{user_id} not found')
        
        if(abs(location[0]-KUMANO_LOCATION[0])>ACCEPTABLE_LOCATION_ERROR[0] or
           abs(location[1]-KUMANO_LOCATION[1])>ACCEPTABLE_LOCATION_ERROR[1]):
            raise UseCaseException('Complete is only available at Kumano Dormitory')
        
        if(target_shift.end_time<datetime.datetime.now() or target_shift.start_time>datetime.datetime.now()):
            raise UseCaseException('This shift is not active now')
        
        shift=target_shift.complete(user)

        group_id=shift.task.group_id
        try:
            member=self.member_repository.find_by_id(group_id,user.id)
        except:
            raise UseCaseException(f'user_id:{user.id} not found in group_id:{group_id}')
        member.point+=shift.task.wage
        user.add_exp(shift.task.id)
       
        _=self.member_repository.save(member)
            
        _=self.user_repository.save(user)
        
        new_shift=self.shift_repository.save(shift)
        return new_shift