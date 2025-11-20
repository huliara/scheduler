from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.shift import IShiftRepository


class ShiftGetUserRelevantUseCase(TransactionUseCaseBase):
    def __init__(self,  shift_repository:IShiftRepository):
        self.shift_repository = shift_repository

    def execute(self, user_id: str):
        return self._transaction(user_id)

    def _transaction(self, user_id: str):
        shifts = self.shift_repository.find_by_user(user_id)
        return shifts