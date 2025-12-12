from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.core.i_repository import IRepository
from ddd.core.i_entity import IEntity
from ddd.domain.user import UserId

class GetUserRelevantUseCase[T:IEntity,U:IRepository](TransactionUseCaseBase):
    def __init__(self,  repository:U):
        self.repository = repository

    def execute(self, user_id: UserId)-> list[T]:
        return self._transaction(user_id)

    def _transaction(self, user_id: UserId):
        shifts = self.repository.find_by_user(user_id)
        return shifts