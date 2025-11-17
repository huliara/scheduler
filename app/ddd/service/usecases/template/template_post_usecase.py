from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.group import IGroupRepository
from app.ddd.domain.task import ITaskRepository
from app.ddd.domain.template import (ITemplateRepository, TemplateEntity,
                                     TemplateSlot)
from app.schemas.template import TemplateCreate


class TemplatePostUseCase(TransactionUseCaseBase):
    
    def __init__(self, db,template_repository:ITemplateRepository,
                 group_repository:IGroupRepository,
                 taskdetail_repository:ITaskRepository):
    
        super().__init__(db)
        self.template_repository=template_repository
        self.group_repository=group_repository
        self.taskdetail_repository=taskdetail_repository
        
    def execute(self,group_id:str,template:TemplateCreate):
        
        return self._transaction(group_id,template)
    
    def _transaction(self,group_id, template:TemplateCreate):
        try:
            group=self.group_repository.find_by_id(group_id)
        except:
            raise UseCaseException(f'group:ID{group_id} not found')
        
        taskdetail_ids=[taskdetail.taskdetail_id for taskdetail in template.slots]
        try:
            taskdetails=self.taskdetail_repository.find_by_ids(taskdetail_ids)
        except:
            raise UseCaseException(f'There are invalid taskdetail_id')
        
        template_entity=TemplateEntity.from_params(
            name=template.name,group_id=group.id,
            slots=[TemplateSlot(
                taskdetail_id=taskdetail.id,
                taskdetail_name=taskdetail.name,
                date_from_start=request_slot.date_from_start,
                start_time=request_slot.start_time
            ) for taskdetail,request_slot in zip(taskdetails,template.slots)]
        )
        
        try:
            template=self.template_repository.add(template_entity)
        except:
            raise UseCaseException('Invalid Template Entity')
        
        return template