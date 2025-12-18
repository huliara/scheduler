from ddd.core.i_entity import IEntity
from ddd.core.i_repository import IRepository
from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.group import GroupId
from ddd.domain.user import UserId

class GetAllUseCase[T:IEntity,U:IRepository](TransactionUseCaseBase):
    def __init__(self,repository:U):
        self.repository=repository
        
    def execute(self,group_id:GroupId|None,user_id:UserId)->list[T]:
        return self._transaction(group_id,user_id)
    
    def _transaction(self,group_id:GroupId|None,user_id:UserId)->list[T]:
        if group_id is None:
            result=self.repository.find_by_user(user_id)
        result=self.repository.find_by_group(group_id)
        return result