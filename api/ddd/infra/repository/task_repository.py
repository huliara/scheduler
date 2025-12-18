
from ddd.core.exception import DomainException
from ddd.domain.task import ITaskRepository, TaskEntity
from ddd.infra.repository import SQLAlchemyBaseRepository
from models.models import SubTask, Task,User
from sqlalchemy.future import select


class TaskRepository(SQLAlchemyBaseRepository,ITaskRepository):

    def find_by_id(self, id):
        model=self.db.get(Task,id)
        return self._refresh_to_entity(model)
    
    def find_by_group(self, group_id):
        models=self.db.scalars(select(Task).filter(Task.group_id==group_id)).all()
        return [self._refresh_to_entity(model) for model in models]
    
    def find_by_user(self, user_id):
        user=self.db.get(User,user_id)
        if user is None:
            raise DomainException('User not found',404)
        joining_group_ids=[group.group_id for group in user.groups]
        tasks=self.db.scalars(select(Task).filter(Task.group_id.in_(joining_group_ids))).all()  
        return [self._refresh_to_entity(task) for task in tasks]
    
    def find_all(self, group_id):
        if group_id is None:
            models=self.db.scalars(select(Task)).all()
            return [self._refresh_to_entity(model) for model in models]
        models=self.db.scalars(select(Task).filter(Task.group_id==group_id)).all()
        return [self._refresh_to_entity(model) for model in models]
    
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
        
        model.subtask=[SubTask(order=index,description=subtask,taskdetail_id=model.id) for index, subtask in enumerate(entity.subtask)]
        
        self.db.commit()
        self.db.refresh(model)
        return self._refresh_to_entity(model)
    
    def remove(self, id):
        model=self.db.get(Task,id)
        if model is None:
            raise DomainException('TaskDetail not found',404)
        self.db.delete(model)
        self.db.commit()
        return self._refresh_to_entity(model)
    
    def _refresh_to_entity(self, model):
        return TaskEntity.from_model(model)