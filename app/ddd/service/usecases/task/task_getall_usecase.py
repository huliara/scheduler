from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import GroupId
from app.ddd.domain.shift import IShiftRepository, Shift


class TaskGetAllUseCase(TransactionUseCaseBase):
    def __init__(self,db,task_repository:IShiftRepository):
        super().__init__(db)
        self.task_repository=task_repository
    
    def execute(self,group_id:GroupId,end:bool|None)->list[Shift]:
        return self._transaction(group_id,end)
    def _transaction(self,group_id,end)->list[Shift]:
        result=self.task_repository.find_all(group_id,end)
        return result