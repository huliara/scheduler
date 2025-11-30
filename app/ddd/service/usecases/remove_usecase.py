from ddd.core.exception import UseCaseException
from ddd.core.i_entity import IEntity
from ddd.core.i_repository import IRepository
from ddd.core.usecase_base import UseCaseBase


class RemoveUseCase[ID,T:IEntity,U:IRepository](UseCaseBase):
    def __init__(self,repository:U):
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