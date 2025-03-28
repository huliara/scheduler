from sqlalchemy.future import select

from app.ddd.core.exception import DomainException
from app.ddd.domain.template import ITemplateRepository, TemplateEntity
from app.models.models import TaskTemplate, Template


class TemplateRepository(ITemplateRepository):
    def __init__(self, db):
        super().__init__(db)        
    def find_by_id(self, id):
        model=self.db.get(Template,id)
        return self._refresh_to_entity(model)
    
    def find_all(self):
        return [self._refresh_to_entity(model) 
                for model in self.db.scalars(select(Template)).all()]
    
    def add(self, entity):
        model=Template(
            name=entity.name,
            group_id=entity.group_id,
            tasktemplates=[
            TaskTemplate(taskdetail_id=slot.taskdetail_id,
                        date_from_start=slot.date_from_start,
                        start_time=slot.start_time) for slot in entity.slots]
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._refresh_to_entity(model)
    
    def save(self, entity):
        model=self.db.get(Template,entity.id)
        if model is None:
            raise DomainException('Template not found',404)
        model.tasktemplates=[
            TaskTemplate(taskdetail_id=slot.taskdetail_id,
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
        if model is None:
            raise DomainException('Template not found',404)
        self.db.delete(model)
        self.db.commit()
        return self._refresh_to_entity(model)
    
    def _refresh_to_entity(self, model):
        entity=TemplateEntity.from_model(model)
        print(entity)
        return entity