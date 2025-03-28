import datetime

from sqlalchemy.orm import Session

from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.task import ITaskRepository, TaskEntity, TaskState
from app.ddd.domain.task_detail import ITaskDetailRepository
from app.ddd.domain.template import (ITemplateRepository, TemplateEntity,
                                     TemplateId)
from app.ddd.domain.user import UserId

from .schema import TaskFromTemplateParams


class TaskFromTemplateUseCase(TransactionUseCaseBase):
    def __init__(self, db:Session,
                 template_repository:ITemplateRepository,
                 task_repository:ITaskRepository,
                 task_detail_repository:ITaskDetailRepository):
        super().__init__(db)
        self.template_repository=template_repository
        self.task_repository=task_repository
        self.taskdetail_repository=task_detail_repository
        
    def execute(self,data:TaskFromTemplateParams)->list[TaskEntity]:
        return self._transaction(data.creater_id,data.template_id,data.start_date)
    
    def _transaction(self,creater_id,tempalte_id:TemplateId,start_date:datetime.date)->list[TaskEntity]:
        template:TemplateEntity=self.template_repository.find_by_id(tempalte_id)
        tasks=self.generate_tasks(creater_id,template,start_date)
        result=self.task_repository.bulk_add(tasks)
        return result
    
    def generate_tasks(self,
                       creater_id:UserId,
                       template:TemplateEntity,
                       start_date:datetime.date,
                       )->list[TaskEntity]:
        tasks = []
        for slot in template.slots:
            taskdetail=self.taskdetail_repository.find_by_id(slot.taskdetail_id)
            date = start_date+datetime.timedelta(days=slot.date_from_start)
            start = datetime.datetime.combine(date, slot.start_time)
            name = (
                str(start.hour)
                + "時"
                + str(start.minute)
                + "分から"
                + str(taskdetail.name)
            )
            task = TaskEntity(
                name=name,
                start_time=start,
                status=TaskState.before_hiring,
                taskdetail=taskdetail.id,
                creater_id=creater_id,
            )
            tasks.append(task)            
        return tasks