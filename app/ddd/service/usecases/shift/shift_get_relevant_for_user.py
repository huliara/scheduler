from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.shift import IShiftRepository
from app.ddd.domain.user import IUserRepository


class ShiftGetUserRelevantUseCase(TransactionUseCaseBase):
    def __init__(self, db, shift_repository:IShiftRepository, user_repository:IUserRepository):
        super().__init__(db)
        self.shift_repository = shift_repository
        self.user_repository = user_repository

    def execute(self, user_id: str):
        return self._transaction(user_id)

    def _transaction(self, user_id: str):
        shifts = self.shift_repository.find_by_user(user_id)
        return shifts