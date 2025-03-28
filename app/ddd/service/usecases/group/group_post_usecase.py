from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import GroupEntity, IGroupRepository


class GroupPostUseCase(TransactionUseCaseBase):
    def __init__(self, db,group_repository:IGroupRepository):
        super().__init__(db)
        self.group_repository=group_repository
        
    def execute(self,name:str):
        group_entity=GroupEntity(name=name)
        return self._transaction(group_entity)
    
    def _transaction(self,entity:GroupEntity)->GroupEntity:
        try:
            group=self.group_repository.add(entity)
        except:
            raise UseCaseException('Invalid Group Entity')
        return group