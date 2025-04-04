from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.template import (ITemplateRepository, TemplateEntity,
                                     TemplateSlot)
from app.schemas.template import TemplateSlotBase


class TemplateUpdateSlotUseCase(TransactionUseCaseBase):
    
    def __init__(self, db,template_repository:ITemplateRepository):
        super().__init__(db)
        self.template_repository=template_repository
        
    def execute(self,template_id:str,prev_slot:TemplateSlotBase,slot:TemplateSlotBase)->TemplateEntity:
        return self._transaction(template_id,prev_slot,slot)
    def _transaction(self,template_id:str,prev_slot:TemplateSlotBase, slot:TemplateSlotBase)->TemplateEntity:
        try:
            template=self.template_repository.find_by_id(template_id)
        except:
            raise UseCaseException(f'template:ID{template_id} not found')
        prev_entity=TemplateSlot(
            taskdetail_id=prev_slot.taskdetail_id,
            date_from_start=prev_slot.date_from_start,
            start_time=prev_slot.start_time
        )
        
        slot_entity=TemplateSlot(
            taskdetail_id=slot.taskdetail_id,
            date_from_start=slot.date_from_start,
            start_time=slot.start_time
        )
        template.delete(prev_entity)
        template.add(slot_entity)
        try:
            new_template=self.template_repository.save(slot)
        except:
            raise UseCaseException('Invalid Template Entity')
        return new_template