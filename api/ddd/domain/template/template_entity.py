from dataclasses import dataclass

import models.models as models
from ddd.core.i_entity import IEntity
from ddd.domain.group.group_value_object import GroupId

from .template_value_object import TemplateId, TemplateSlot


@dataclass
class TemplateEntity(IEntity):
    id:TemplateId|None
    name:str
    slots:set[TemplateSlot]
    group_id:GroupId
    group_name:str|None=None

    @classmethod
    def from_model(cls, data:"models.Template") -> 'TemplateEntity':
        return cls(
            id=TemplateId(data.id),
            name=data.name,
            slots=set([
                TemplateSlot(task_id=slot.task_id,
                             task_name=slot.task.name if slot.task else "",
                             date_from_start=slot.date_from_start,
                             start_time=slot.start_time) 
                for slot in data.tasktemplates]),
            group_id=GroupId(data.group_id),
            group_name=data.group.name if data.group else None
        )
    @classmethod
    def from_params(cls, name:str, group_id:GroupId, slots:list[TemplateSlot]) -> 'TemplateEntity':
        return cls(
            id=None,
            name=name,
            group_id=group_id,
            slots=set(slots)
        )
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slots': 
                [slot.to_dict() for slot in self.slots],
            'group_id': self.group_id,
            'group_name': self.group_name
        }
    def add(self,slot:TemplateSlot):
        self.slots.add(slot)
        
    def delete(self,target_slot:TemplateSlot):
        self.slots=[slot  for slot in self.slots if slot!=target_slot]