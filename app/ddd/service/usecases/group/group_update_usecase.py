from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import GroupEntity, IGroupRepository


class GroupUpdateUseCase(TransactionUseCaseBase):
    def __init__(self, db,group_repository:IGroupRepository):
        super().__init__(db)
        self.group_repository=group_repository
        
    def execute(self,group:GroupEntity):
        return self._transaction(group)
    
    def _transaction(self,group:GroupEntity)->GroupEntity:
        try:
            _=self.group_repository.find_by_id(group.id)
        except:
            raise UseCaseException(f'group_id:{group.id} not found')
        new_group=self.group_repository.update(group)
        return new_group