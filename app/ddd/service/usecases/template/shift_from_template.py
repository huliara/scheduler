import datetime

from sqlalchemy.orm import Session

from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.shift import IShiftRepository, ShiftEntity, ShiftState
from app.ddd.domain.task import ITaskRepository
from app.ddd.domain.template import (ITemplateRepository, TemplateEntity,
                                     TemplateId)
from app.ddd.domain.user import UserId

from .schema import ShiftFromTemplateParams


class ShiftFromTemplateUseCase(TransactionUseCaseBase):
    def __init__(self,
                 template_repository:ITemplateRepository,
                 shift_repository:IShiftRepository,
                 task_repository:ITaskRepository):
        self.template_repository=template_repository
        self.shift_repository=shift_repository
        self.task_repository=task_repository
        
    def execute(self,data:ShiftFromTemplateParams)->list[ShiftEntity]:
        return self._transaction(data.creater_id,data.template_id,data.start_date)
    
    def _transaction(self,creater_id,tempalte_id:TemplateId,start_date:datetime.date)->list[ShiftEntity]:
        template:TemplateEntity=self.template_repository.find_by_id(tempalte_id)
        shifts=self.generate_shifts(creater_id,template,start_date)
        result=self.shift_repository.bulk_add(shifts)
        return result
    
    def generate_shifts(self,
                       creater_id:UserId,
                       template:TemplateEntity,
                       start_date:datetime.date,
                       )->list[ShiftEntity]:
        shifts = []
        for slot in template.slots:
            task=self.task_repository.find_by_id(slot.task_id)
            date = start_date+datetime.timedelta(days=slot.date_from_start)
            start = datetime.datetime.combine(date, slot.start_time)
            name = (
                str(start.hour)
                + "時"
                + str(start.minute)
                + "分から"
                + str(task.name)
            )
            shift = ShiftEntity(
                id=None,
                name=name,
                start_time=start,
                status=ShiftState.hiring,
                task=task,
                creater_id=creater_id,
            )
            shifts.append(shift)            
        return shifts