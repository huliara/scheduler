from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.group import GroupEntity, IGroupRepository


class GroupGetAllUseCase(TransactionUseCaseBase):
    def __init__(self, group_repository: IGroupRepository):
        self.group_repository = group_repository

    def execute(self) -> list[GroupEntity]:
        return self._transaction()

    def _transaction(self) -> list[GroupEntity]:
        result = self.group_repository.find_all()
        return result