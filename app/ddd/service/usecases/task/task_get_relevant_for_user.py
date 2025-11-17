from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.shift import IShiftRepository
from app.ddd.domain.user import IUserRepository


class TaskGetUserRelevantUseCase(TransactionUseCaseBase):
    def __init__(self, db, task_repository:IShiftRepository, user_repository:IUserRepository):
        super().__init__(db)
        self.task_repository = task_repository
        self.user_repository = user_repository

    def execute(self, user_id: str):
        return self._transaction(user_id)

    def _transaction(self, user_id: str):
        tasks = self.task_repository.find_by_user(user_id)
        return tasks