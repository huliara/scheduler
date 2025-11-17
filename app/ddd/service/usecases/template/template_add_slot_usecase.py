from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.task import ITaskRepository
from app.ddd.domain.template import (ITemplateRepository, TemplateEntity,
                                     TemplateSlot)
from app.schemas.template import TemplateSlotBase


class TemplateAddSlotUseCase(TransactionUseCaseBase):
    
    def __init__(self, db,template_repository:ITemplateRepository,taskdetail_repository:ITaskRepository):
        super().__init__(db)
        self.template_repository=template_repository
        self.taskdetail_repository=taskdetail_repository
        
    def execute(self,template_id:str,slot:TemplateSlotBase)->TemplateEntity:
        return self._transaction(template_id,slot)
    def _transaction(self, template_id:str,slot:TemplateSlotBase)->TemplateEntity:
        try:
            template=self.template_repository.find_by_id(template_id)
        except:
            raise UseCaseException(f'template:ID{template_id} not found')
        
        try:
            taskdetail=self.taskdetail_repository.find_by_id(slot.taskdetail_id)
        except:
            raise UseCaseException(f'taskdetail:ID{slot.taskdetail_id} not found')
        
        slot_entity=TemplateSlot(
            taskdetail_id=slot.taskdetail_id,
            taskdetail_name=taskdetail.name,
            date_from_start=slot.date_from_start,
            start_time=slot.start_time
        )
        template.add(slot_entity)
        try:
            new_template=self.template_repository.save(template)
        except:
            raise UseCaseException('Invalid Template Entity')
        return new_template