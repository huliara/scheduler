from sqlalchemy.future import select

from ddd.core.exception import DomainException
from ddd.domain.template import ITemplateRepository, TemplateEntity
from models.models import TaskTemplate, Template


class TemplateRepository(ITemplateRepository):
    def __init__(self, db):
        super().__init__(db)        
    def find_by_id(self, id):
        model=self.db.get(Template,id)
        return self._refresh_to_entity(model)
    
    def find_all(self,group_id):
        if group_id is None:
            return [self._refresh_to_entity(model) 
                    for model in self.db.scalars(select(Template)).all()]
        return [self._refresh_to_entity(model) 
                for model in self.db.scalars(select(Template).filter(Template.group_id==group_id)).all()]
    
    def add(self, entity):
        model=Template(
            name=entity.name,
            group_id=entity.group_id
        )
        for slot in entity.slots:
            model_slot=TaskTemplate(task_id=slot.task_id,
                                                    date_from_start=slot.date_from_start,
                                                    start_time=slot.start_time)
            model.tasktemplates.append(model_slot)
        
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._refresh_to_entity(model)
    
    def save(self, entity):
        model=self.db.get(Template,entity.id)
        if model is None:
            raise DomainException('Template not found',404)
        for slot in model.tasktemplates:
            self.db.delete(slot)
        model.name=entity.name
        model.tasktemplates=[
            TaskTemplate(
                template_id=model.id,
                task_id=slot.task_id,
                        date_from_start=slot.date_from_start,
                        start_time=slot.start_time) for slot in entity.slots]
        self.db.commit()
        self.db.refresh(model)
        return self._refresh_to_entity(model)
    
    def update_name(self, id, name):
        model=self.db.get(Template,id)
        if model is None:
            raise DomainException('Template not found',404)
        model.name=name
        self.db.commit()
        self.db.refresh(model)
        return self._refresh_to_entity(model)
    
    def remove(self, id):
        model=self.db.get(Template,id)
        resposnse=self._refresh_to_entity(model)
        if model is None:
            raise DomainException('Template not found',404)
        self.db.delete(model)
        self.db.commit()
        return resposnse
    
    def _refresh_to_entity(self, model):
        entity=TemplateEntity.from_model(model)
        print(entity)
        return entity