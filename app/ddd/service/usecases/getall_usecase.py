from sqlalchemy.orm import Session

from app.ddd.core.i_entity import IEntity
from app.ddd.core.i_repository import IRepository
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import GroupId


class GetAllUseCase[T:IEntity,U:IRepository](TransactionUseCaseBase):
    def __init__(self,db:Session,repository:U):
        super().__init__(db)
        self.repository=repository
        
    def execute(self,group_id:GroupId|None)->list[T]:
        return self._transaction(group_id)
    
    def _transaction(self,group_id:GroupId|None)->list[T]:
        result=self.repository.find_all(group_id)
        return result