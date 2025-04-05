import datetime
from dataclasses import dataclass

import app.models.models as models
from app.ddd.core.i_entity import IEntity
from app.ddd.domain.group.group_value_object import GroupId

from .template_value_object import TemplateId, TemplateSlot


@dataclass
class TemplateEntity(IEntity):
    id:TemplateId|None
    name:str
    slots:set[TemplateSlot]
    group_id:GroupId
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }
    @classmethod
    def from_model(cls, data:"models.Template") -> 'TemplateEntity':
        return cls(
            id=TemplateId(data.id),
            name=data.name,
            slots=[
                TemplateSlot(taskdetail_id=slot.taskdetail_id,
                             taskdetail_name=slot.taskdetail.name,
                             date_from_start=slot.date_from_start,
                             start_time=slot.start_time) 
                for slot in data.tasktemplates],
            group_id=GroupId(data.group_id),
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
                [{
                    'id':f'{slot.taskdetail_id}#{slot.start_time}#{slot.date_from_start}',
                    'taskdetail_id':slot.taskdetail_id,
                    'name':slot.name,
                  'date_from_start':slot.date_from_start,
                  'start_time':slot.start_time} 
                 for slot in self.slots],
            'group_id': self.group_id
        }
    def add(self,slot:TemplateSlot):
        self.slots.add(slot)
        
    def delete(self,slot:TemplateSlot):
        self.slots=[slot  for slot in self.slots if slot!=slot]