from app.ddd.domain.group.group_value_object import GroupId
from app.ddd.domain.template.template_value_object import TemplateSlot


class TemplateCreateParams:
    name:str
    group_id:GroupId
    tasks:set[TemplateSlot]
