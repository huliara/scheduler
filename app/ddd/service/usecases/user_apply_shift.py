from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.shift import IShiftRepository, ShiftId
from ddd.domain.user import IUserRepository, UserId
from sqlalchemy.orm import Session


class UserApplyShiftUseCase(TransactionUseCaseBase):
    
    def __init__(self, db: Session,
                 user_repository:IUserRepository,
                 shift_repository:IShiftRepository) -> None:
        super().__init__(db)
        self.user_repository:IUserRepository = user_repository
        self.shift_reposiotry:IShiftRepository = shift_repository
        
    def execute(self, user_id:UserId, shift_id:ShiftId) :
        return self._transaction(user_id, shift_id)
        
    def _transaction(self, user_id: UserId, shift_id:ShiftId) -> None:
        user=self.user_repository.find_by_id(user_id)
        shift=self.shift_reposiotry.find_by_id(shift_id)
        shift.add(user)
        _=self.shift_reposiotry.save(shift)
        return self.user_repository.find_by_id(user.id)
