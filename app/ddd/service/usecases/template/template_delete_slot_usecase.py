from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.task import ITaskRepository
from app.ddd.domain.template import (ITemplateRepository, TemplateEntity,
                                     TemplateSlot)
from app.schemas.template import TemplateSlotBase


class TemplateDeleteSlotUseCase(TransactionUseCaseBase):
    
    def __init__(self, db,template_repository:ITemplateRepository,task_repository:ITaskRepository):
        super().__init__(db)
        self.template_repository=template_repository
        self.task_repository=task_repository
        
    def execute(self,template_id:str,slot:TemplateSlotBase)->TemplateEntity:
        return self._transaction(template_id,slot)
    def _transaction(self, template_id:str,slot:TemplateSlotBase)->TemplateEntity:
        try:
            template=self.template_repository.find_by_id(template_id)
        except:
            raise UseCaseException(f'template:ID{template_id} not found')
        try:
            task=self.task_repository.find_by_id(slot.task_id)
        except:
            raise UseCaseException(f'task:ID{slot.task_id} not found')
        
        
        slot_entity=TemplateSlot(
            task_id=slot.task_id,
            task_name=task.name,
            date_from_start=slot.date_from_start,
            start_time=slot.start_time
        )
        template.delete(slot_entity)
        try:
            new_template=self.template_repository.save(template)
        except:
            raise UseCaseException('Invalid Template Entity')
        return new_template