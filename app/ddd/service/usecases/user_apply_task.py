from sqlalchemy.orm import Session

from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.shift import IShiftRepository, ShiftId
from app.ddd.domain.user import IUserRepository, UserId


class UserApplyTaskUseCase(TransactionUseCaseBase):
    
    def __init__(self, db: Session,
                 user_repository:IUserRepository,
                 task_repository:IShiftRepository) -> None:
        super().__init__(db)
        self.user_repository:IUserRepository = user_repository
        self.task_reposiotry:IShiftRepository = task_repository
        
    def execute(self, user_id:UserId, task_id:ShiftId) :
        return self._transaction(user_id, task_id)
        
    def _transaction(self, user_id: UserId, task_id:ShiftId) -> None:
        user=self.user_repository.find_by_id(user_id)
        task=self.task_reposiotry.find_by_id(task_id)
        task.add(user)
        _=self.task_reposiotry.save(task)
        return self.user_repository.find_by_id(user.id)
