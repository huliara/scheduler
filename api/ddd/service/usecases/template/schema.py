import datetime
from dataclasses import dataclass

from ddd.domain.template import TemplateId
from ddd.domain.user import UserId


@dataclass
class ShiftFromTemplateParams:
    creater_id:UserId
    template_id:TemplateId
    start_date:datetime.date
    add_default_worker:bool=False
    
