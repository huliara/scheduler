import datetime

from app.ddd.domain.template import TemplateId
from app.ddd.domain.user import UserId


class TaskFromTemplateParams:
    creater_id:UserId
    template_id:TemplateId
    start_date:datetime.date