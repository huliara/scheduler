from sqlalchemy.future import select

from app.ddd.core.exception import DomainException
from app.ddd.domain.task import ITaskRepository, TaskEntity, TaskId
from app.models.models import Task


class TaskRepository(ITaskRepository):
    
    def __init__(self, db):
        super().__init__(db)
        
    def find_by_id(self, id):
        model=self.db.get(Task,id)
        return self._refresh_to_entity(model)
    
    def find_all(self):
        return [self._refresh_to_entity(model) 
                for model in self.db.scalars(select(Task)).all()]
        
    def add(self, entity: TaskEntity):
        model=Task(
            name=entity.name,
            start_time=entity.start_time,
            creater_id=entity.creater_id,
            taskdetail_id=entity.taskdetail.id,
        )
        self.db.add(model)
        self.db.commit()
        return self._refresh_to_entity(model)
    
    def update(self, entity: TaskEntity):
        model=self.db.get(Task,entity.id)
        if model is None:
            raise DomainException('Task not found',404)
        model.name=entity.name
        model.start_time=entity.start_time
        model.creater_id=entity.creater_id
        model.taskdetail_id=entity.taskdetail.id
        self.db.commit()
        return self._refresh_to_entity(model)

    def remove(self, id: TaskId):
        model=self.db.get(Task,id)
        if model is None:
            raise DomainException('Task not found',404)
        self.db.delete(model)
        self.db.commit()
        return self._refresh_to_entity(model)
    
    
    def _refresh_to_entity(self, model: Task) -> TaskEntity:
        entity=TaskEntity.from_model(model)
        return entity