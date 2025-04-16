import datetime

from sqlalchemy import delete, insert
from sqlalchemy.future import select

from app.ddd.core.exception import DomainException
from app.ddd.domain.task import ITaskRepository, TaskEntity, TaskId
from app.models.models import Task, User


class TaskRepository(ITaskRepository):
    
    def __init__(self, db):
        self.db = db
        
    def find_by_id(self, id):
        model=self.db.get(Task,id)
        return self.refresh_to_entity(model)
    
    def find_all(self,group_id:str,end:bool|None=None):
        if end is not None:
            return [self.refresh_to_entity(model) 
                    for model in self.db.scalars(select(Task).filter(Task.end_time<datetime.datetime.now())).all()]
        return [self.refresh_to_entity(model) 
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
        return self.refresh_to_entity(model)
    
    def bulk_add(self, tasks):
        data=[{'name':entity.name,
               'start_time':entity.start_time,
               'status':entity.status,
               'creater_id':entity.creater_id,
               'taskdetail_id':entity.taskdetail.id,
               'group_id':entity.group_id} for entity in tasks]
        result=self.db.scalars(insert(Task).returning(Task),data).all()
        self.db.commit()
        for model in result:
            self.db.refresh(model)
        return [self.refresh_to_entity(model) for model in result]
    
    def bulk_remove(self, tasks):
        self.db.execute(delete(Task).where(Task.id.in_([task.id for task in tasks])))
        self.db.commit()
        return 
    
    def find_by_ids(self, ids):
        tasks=self.db.scalars(select(Task).filter(Task.id.in_(ids))).all()
        return [self.refresh_to_entity(task) for task in tasks]
    
    def save(self, entity: TaskEntity):
        model=self.db.get(Task,entity.id)
        if model is None:
            raise DomainException('Task not found',404)
        model.name=entity.name
        model.start_time=entity.start_time
        model.creater_id=entity.creater_id
        model.taskdetail_id=entity.taskdetail.id
        self.db.commit()
        self.db.refresh(model)
        return self.refresh_to_entity(model)

    def remove(self, id: TaskId):
        model=self.db.get(Task,id)
        if model is None:
            raise DomainException('Task not found',404)
        self.db.delete(model)
        self.db.commit()
        return TaskEntity(
            id=model.id,
            name=model.name,
            start_time=model.start_time,
            status=model.status,
            taskdetail=None,
            workers=[],
            creater_id=model.creater_id,
        )
    
    def find_by_user(self, user_id):
        user=self.db.get(User,user_id)
        if user is None:
            raise DomainException('User not found',404)
        joining_group_ids=[group.id for group in user.groups]
        tasks=self.db.scalars(select(Task).filter(Task.group_id.in_(joining_group_ids))).all()

        return{
            "assign": [self.refresh_to_entity(task) for task in tasks if user in task.workers and task.end_time>datetime.datetime.now() and (task.status!=0 or task.status!=3)],
            "hiring":[self.refresh_to_entity(task) for task in tasks if user not in task.workers and task.end_time>datetime.datetime.now() and (task.status!=0 or task.status!=3)],
            "end":[self.refresh_to_entity(task) for task in tasks if user in task.workers and task.end_time<datetime.datetime.now() and task.status!=3],
        }
    
    
    def refresh_to_entity(self, model: Task) -> TaskEntity:
        entity=TaskEntity.from_model(model)
        return entity