from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import IGroupRepository
from app.ddd.domain.task import ITaskRepository
from app.ddd.domain.template import (ITemplateRepository, TemplateEntity,
                                     TemplateSlot)
from app.schemas.template import TemplateCreate


class TemplatePostUseCase(TransactionUseCaseBase):
    
    def __init__(self, template_repository:ITemplateRepository,
                 group_repository:IGroupRepository,
                 task_repository:ITaskRepository):
        self.template_repository=template_repository
        self.group_repository=group_repository
        self.task_repository=task_repository
        
    def execute(self,template:TemplateCreate):
        
        return self._transaction(template.group_id,template)
    
    def _transaction(self,group_id, template:TemplateCreate):
        try:
            group=self.group_repository.find_by_id(group_id)
        except:
            raise UseCaseException(f'group:ID{group_id} not found')
        
        task_ids=[slot.task_id for slot in template.slots]
        try:
            tasks=self.task_repository.find_by_ids(task_ids)
        except:
            raise UseCaseException(f'There are invalid task_id')
        
        template_entity=TemplateEntity.from_params(
            name=template.name,group_id=group.id,
            slots=[TemplateSlot(
                task_id=task.id,
                task_name=task.name,
                date_from_start=request_slot.date_from_start,
                start_time=request_slot.start_time
            ) for task,request_slot in zip(tasks,template.slots)]
        )
        
        try:
            template=self.template_repository.add(template_entity)
        except:
            raise UseCaseException('Invalid Template Entity')
        
        return template