from ddd.core.exception import UseCaseException
from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.group import GroupEntity, IGroupRepository


class GroupPostUseCase(TransactionUseCaseBase):
    def __init__(self, group_repository:IGroupRepository):
        self.group_repository=group_repository
        
    def execute(self,name:str):
        group_entity=GroupEntity(id=None,name=name)
        return self._transaction(group_entity)
    
    def _transaction(self,entity:GroupEntity)->GroupEntity:
        try:
            group=self.group_repository.add(entity)
        except:
            raise UseCaseException('Invalid Group Entity')
        return group