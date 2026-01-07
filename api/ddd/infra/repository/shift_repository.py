import datetime

from ddd.core.exception import DomainException
from ddd.domain.shift import IShiftRepository, ShiftEntity, ShiftId
from ddd.infra.repository import SQLAlchemyBaseRepository
from models.models import Shift, User
from sqlalchemy import delete, insert
from sqlalchemy.future import select


class ShiftRepository(SQLAlchemyBaseRepository[ShiftEntity],IShiftRepository):
    
    def find_by_id(self, id):
        model=self.db.get(Shift,id)
        return self._refresh_to_entity(model)
    
    def find_by_group(self, group_id):
        models=self.db.scalars(select(Shift).filter(Shift.group_id==group_id)).all()
        return [self._refresh_to_entity(model) for model in models]
    
    def find_by_user(self, user_id):
        user=self.db.get(User,user_id)
        if user is None:
            raise DomainException('User not found',404)
        joining_group_ids=[group.group_id for group in user.groups]
        shifts=self.db.scalars(select(Shift).filter(Shift.group_id.in_(joining_group_ids))).all()

        return [self._refresh_to_entity(shift) for shift in shifts]
    
    def find_all(self,end:bool|None=None):
        if end is not None:
            return [self._refresh_to_entity(model) 
                    for model in self.db.scalars(select(Shift).filter(Shift.end_time<datetime.datetime.now())).all()]
        return [self._refresh_to_entity(model) 
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
        return self._refresh_to_entity(model)
    
    def bulk_add(self, shifts):
        data=[{'name':entity.name,
               'start_time':entity.start_time,
               'creater_id':entity.creater_id,
               'task_id':entity.task.id,
               'group_id':entity.group_id} for entity in shifts]
        result=self.db.scalars(insert(Shift).returning(Shift),data).all()
        self.db.commit()
        for model in result:
            self.db.refresh(model)
        return [self._refresh_to_entity(model) for model in result]
    
    def bulk_remove(self, shifts):
        self.db.execute(delete(Shift).where(Shift.id.in_([task.id for task in shifts])))
        self.db.commit()
        return 
    
    def bulk_update(self, shifts):
        for shift in shifts:
            self.save(shift)
        return shifts
    
    def find_by_ids(self, ids):
        tasks=self.db.scalars(select(Shift).filter(Shift.id.in_(ids))).all()
        return [self._refresh_to_entity(task) for task in tasks]
    
    def save(self, entity: ShiftEntity):
        model=self.db.get(Shift,entity.id)
        if model is None:
            raise DomainException('Shift not found',404)
        model.name=entity.name
        model.start_time=entity.start_time
        model.creater_id=entity.creater_id
        model.task_id=entity.task.id
        worker_ids=[user.id for user in entity.workers]
        model.workers=[user for user in self.db.scalars(select(User).filter(User.id.in_(worker_ids))).all()]
        self.db.commit()
        self.db.refresh(model)
        return self._refresh_to_entity(model)

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
            task=None,
            workers=[],
            creater_id=model.creater_id,
        )
    
    
    def _refresh_to_entity(self, model: Shift) -> ShiftEntity:
        entity=ShiftEntity.from_model(model)
        return entity