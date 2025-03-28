from sqlalchemy.orm import Session

from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.task import ITaskRepository, TaskEntity, TaskId
from app.ddd.domain.task_detail import ITaskDetailRepository
from app.schemas.task import TaskCreate


class TaskUpdateUseCase(TransactionUseCaseBase):
    def __init__(self,db:Session,
                 task_repository:ITaskRepository,
                 taskdetail_repository:ITaskDetailRepository
                 ):
        super().__init__(db)
        self.task_repository=task_repository
        self.taskdetail_repository=taskdetail_repository
        
    def execute(self,task_id:TaskId, request:TaskCreate)->TaskEntity:
        return self._transaction(task_id,request)
    def _transaction(self,task_id:TaskId,request:TaskCreate)->TaskEntity:
        try:
            target_task=self.task_repository.find_by_id(task_id)
        except:
            raise UseCaseException('taskdetail_id:f{task_id} not found')
        try:
            taskdetail=self.taskdetail_repository.find_by_id(request.taskdetail_id)
        except:
            raise UseCaseException('taskdetail_id:f{request.taskdetail_id} not found')
        target_task.name=request.name
        target_task.start_time=request.start_time
        target_task.taskdetail=taskdetail
        task_new=self.task_repository.save(task_id,target_task)
        
        return task_new