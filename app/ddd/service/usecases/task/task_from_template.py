import datetime

from sqlalchemy.orm import Session

from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.task import ITaskRepository, TaskEntity
from app.ddd.domain.template import ITemplateRepository, TemplateId


class TaskFromTemplateUseCase(TransactionUseCaseBase):
    def __init__(self, db:Session,
                 template_repository:ITemplateRepository,
                 task_repository:ITaskRepository):
        super().__init__(db)
        self.template_repository=template_repository
        self.task_repository=task_repository
        
    def execute(self, template_id:TemplateId,start_date:datetime.date)->list[TaskEntity]:
        return self._transaction(template_id,start_date)
    def _transaction(self,tempalte_id:TemplateId,start_date:datetime.date)->list[TaskEntity]:
        
        return 