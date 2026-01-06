
from ddd.core.exception import DomainException
from ddd.domain.task.task_repository import ITaskRepository
from ddd.domain.task.task_entity import TaskEntity
from ddd.infra.repository import SQLAlchemyBaseRepository
from models.models import SubTask, Task
from sqlalchemy.future import select


class TaskRepository(SQLAlchemyBaseRepository[TaskEntity],ITaskRepository):

    def __init__(self, db):
        super().__init__(db)
        self.Model=Task
        self.Entity=TaskEntity
        
    def find_by_ids(self, ids):
        models=self.db.scalars(select(Task).filter(Task.id.in_(ids))).all()
        return [self._refresh_to_entity(model) for model in models]
    def add(self, entity: TaskEntity):
        model=Task(
            name=entity.name,
            subtask=[SubTask(order=index,description=subtask) for index, subtask in enumerate(entity.subtask)],
            max_worker=entity.max_worker,
            min_worker=entity.min_worker,
            exp_worker=entity.exp_worker,
            duration=entity.duration,
            group_id=entity.group_id,
            wage=entity.wage,
            permissions=entity.permissions,
            creater_id=entity.creater_id,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._refresh_to_entity(model)
    def save(self, entity: TaskEntity):
        model=self.db.get(Task,entity.id)
        if model is None:
            raise DomainException('TaskDetail not found',404)
        model.name=entity.name
        model.max_worker=entity.max_worker
        model.min_worker=entity.min_worker
        model.exp_worker=entity.exp_worker
        model.duration=entity.duration
        model.wage=entity.wage
        model.permissions=entity.permissions
        model.group_id=entity.group_id
        model.subtask=[SubTask(order=index,description=subtask,task_id=model.id) for index, subtask in enumerate(entity.subtask)]
        
        self.db.commit()
        self.db.refresh(model)
        return self._refresh_to_entity(model)
