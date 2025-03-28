import datetime
from dataclasses import dataclass

from app.ddd.domain.template import TemplateId
from app.ddd.domain.user import UserId


@dataclass
class TaskFromTemplateParams:
    creater_id:UserId
    template_id:TemplateId
    start_date:datetime.date
