import datetime

from ddd.core.exception import DomainException
from ddd.domain.shift import IShiftRepository, ShiftEntity, ShiftId, ShiftState
from models.models import Shift, User
from sqlalchemy import delete, insert
from sqlalchemy.future import select
from sqlalchemy.orm import Session


class ShiftRepository(IShiftRepository):
    
    def __init__(self, db:Session):
        self.db = db
        
    def find_by_id(self, id):
        model=self.db.get(Shift,id)
        return self.refresh_to_entity(model)
    
    def find_all(self,group_id:str,end:bool|None=None):
        if end is not None:
            return [self.refresh_to_entity(model) 
                    for model in self.db.scalars(select(Shift).filter(Shift.end_time<datetime.datetime.now())).all()]
        return [self.refresh_to_entity(model) 
                for model in self.db.scalars(select(Shift)).all()]
        
    def add(self, entity: ShiftEntity):
        model=Shift(
            name=entity.name,
            start_time=entity.start_time,
            creater_id=entity.creater_id,
            taskdetail_id=entity.task.id,
        )
        self.db.add(model)
        self.db.commit()
        return self.refresh_to_entity(model)
    
    def bulk_add(self, shifts):
        data=[{'name':entity.name,
               'start_time':entity.start_time,
               'status':entity.status,
               'creater_id':entity.creater_id,
               'task_id':entity.task.id,
               'group_id':entity.group_id} for entity in shifts]
        result=self.db.scalars(insert(Shift).returning(Shift),data).all()
        self.db.commit()
        for model in result:
            self.db.refresh(model)
        return [self.refresh_to_entity(model) for model in result]
    
    def bulk_remove(self, tasks):
        self.db.execute(delete(Shift).where(Shift.id.in_([task.id for task in tasks])))
        self.db.commit()
        return 
    
    def find_by_ids(self, ids):
        tasks=self.db.scalars(select(Shift).filter(Shift.id.in_(ids))).all()
        return [self.refresh_to_entity(task) for task in tasks]
    
    def save(self, entity: ShiftEntity):
        model=self.db.get(Shift,entity.id)
        if model is None:
            raise DomainException('Shift not found',404)
        model.name=entity.name
        model.start_time=entity.start_time
        model.creater_id=entity.creater_id
        model.task_id=entity.task.id
        model.status=entity.status
        worker_ids=[user.id for user in entity.workers]
        model.workers=[user for user in self.db.scalars(select(User).filter(User.id.in_(worker_ids))).all()]
        self.db.commit()
        self.db.refresh(model)
        return self.refresh_to_entity(model)

    def remove(self, id: ShiftId):
        model=self.db.get(Shift,id)
        if model is None:
            raise DomainException('Shift not found',404)
        self.db.delete(model)
        self.db.commit()
        return ShiftEntity(
            id=model.id,
            name=model.name,
            start_time=model.start_time,
            status=model.status,
            task=None,
            workers=[],
            creater_id=model.creater_id,
        )
    
    def find_by_user(self, user_id):
        user=self.db.get(User,user_id)
        if user is None:
            raise DomainException('User not found',404)
        joining_group_ids=[group.group_id for group in user.groups]
        tasks=self.db.scalars(select(Shift).filter(Shift.group_id.in_(joining_group_ids))).all()

        return{
            "assign": [self.refresh_to_entity(task) for task in tasks 
                       if user in task.workers and task.end_time>datetime.datetime.now() and (task.status!=0 or task.status!=3)],
            "hiring":[self.refresh_to_entity(task) for task in tasks 
                      if user not in task.workers and task.end_time>datetime.datetime.now() and (task.status!=0 or task.status!=3)],
            "end":[self.refresh_to_entity(task) for task in tasks 
                   if user in task.workers and task.end_time<datetime.datetime.now() and task.status!=ShiftState.archive],
        }
    
    
    def refresh_to_entity(self, model: Shift) -> ShiftEntity:
        entity=ShiftEntity.from_model(model)
        return entity