import datetime
from abc import abstractmethod

import models.models as models
from ddd.core.i_repository import IRepository
from ddd.domain.group import GroupId
from ddd.domain.task import TaskId
from ddd.domain.user import UserId

from .shift_entity import ShiftEntity
from .shift_value_object import ShiftId


class IShiftRepository(IRepository[ShiftEntity,ShiftId]):
    @abstractmethod
    def add(self,name:str,start_time:datetime.datetime,creater_id:UserId,task_id:TaskId)->ShiftEntity:
        pass
    
    @abstractmethod
    def save(self,shift:ShiftEntity)->ShiftEntity:
        pass
    
    @abstractmethod
    def find_all(self,group_id:GroupId,end:bool|None)->list[ShiftEntity]:
        pass

    @abstractmethod
    def refresh_to_entity(self, model:"models.Shift") -> ShiftEntity:
        pass
    
    @abstractmethod
    def bulk_add(self,shifts:list[ShiftEntity])->list[ShiftEntity]:
        pass
    
    @abstractmethod
    def bulk_remove(self,shifts:list[ShiftEntity])->list[ShiftEntity]:
        pass
    
    @abstractmethod
    def find_by_ids(self,ids:list[ShiftId])->list[ShiftEntity]:
        pass
    
    @abstractmethod
    def find_by_user(self,user_id:UserId)->list[ShiftEntity]:
        pass