from ddd.core.exception import UseCaseException
from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.group import IGroupRepository
from ddd.domain.task.task_repository import ITaskRepository
from ddd.domain.template import (ITemplateRepository, TemplateEntity,
                                     TemplateSlot)
from schemas.template import TemplateCreate


class TemplatePostUseCase(TransactionUseCaseBase):
    
    def __init__(self, template_repository:ITemplateRepository,
                 group_repository:IGroupRepository,
                 task_repository:ITaskRepository):
        self.template_repository=template_repository
        self.group_repository=group_repository
        self.task_repository=task_repository
        
    def execute(self,template:TemplateCreate):
        
        return self._transaction(template.group_id,template)
    
    def _transaction(self,group_id, request:TemplateCreate):
        try:
            group=self.group_repository.find_by_id(group_id)
        except:
            raise UseCaseException(f'group:ID{group_id} not found')
        
        task_ids=[slot.task_id for slot in request.slots]
        try:
            tasks=self.task_repository.find_by_ids(task_ids)
        except:
            raise UseCaseException(f'There are invalid task_id')
        
        template_entity=TemplateEntity.from_params(
            name=request.name,group_id=group.id,
            slots=[TemplateSlot(
                task_id=slot.task_id,
                date_from_start=slot.date_from_start,
                start_time=slot.start_time
            ) for slot in request.slots]
        )
        
        try:
            request=self.template_repository.add(template_entity)
        except:
            raise UseCaseException('Invalid Template Entity')
        
        return request