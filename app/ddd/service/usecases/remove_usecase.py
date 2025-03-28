from app.ddd.core.exception import UseCaseException
from app.ddd.core.i_entity import IEntity
from app.ddd.core.i_repository import IRepository
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase


class RemoveUseCase[ID,T:IEntity,U:IRepository](TransactionUseCaseBase):
    def __init__(self, db,repository:U):
        super().__init__(db)
        self.repository=repository
        
    def execute(self,entity_id:ID):
        return self._transaction(entity_id)
    
    def _transaction(self,id:ID)->T:
        try:
            _=self.repository.find_by_id(id)
        except:
            raise UseCaseException(f'{ID.__name__}:{id} not found')
        result=self.repository.remove(id)
        return result