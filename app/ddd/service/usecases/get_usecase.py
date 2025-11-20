
from app.ddd.core.exception import UseCaseException
from app.ddd.core.i_entity import IEntity
from app.ddd.core.i_repository import IRepository
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase


class GetUseCase[ID,T:IEntity,U:IRepository](TransactionUseCaseBase):
    def __init__(self,repository:U):
        self.repository=repository
        
    def execute(self,id:ID)->T:
        return self._transaction(id)
    
    def _transaction(self,id:ID)->T:
        try:
            result=self.repository.find_by_id(id)
        except:
            raise  UseCaseException(f'{ID.__name__}:{id} not found')
        return result