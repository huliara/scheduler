import datetime
from abc import abstractmethod

import app.ddd.domain.group as group
import app.ddd.domain.user as user
import app.models.models as models
from app.ddd.core.i_repository import IRepository
from app.ddd.domain.task_detail import TaskDetailId

from .task_entity import TaskEntity
from .task_value_object import TaskId


class ITaskRepository(IRepository[TaskEntity,TaskId]):
    @abstractmethod
    def add(self,name:str,start_time:datetime.datetime,creater_id:'user.UserId',taskdetail_id:TaskDetailId)->TaskEntity:
        pass
    
    @abstractmethod
    def save(self,task:TaskEntity)->TaskEntity:
        pass
    
    @abstractmethod
    def find_all(self,group_id:'group.GroupId',end:bool|None)->list[TaskEntity]:
        pass

    @abstractmethod
    def refresh_to_entity(self, model:"models.Task") -> TaskEntity:
        pass
    
    @abstractmethod
    def bulk_add(self,tasks:list[TaskEntity])->list[TaskEntity]:
        pass
    
    @abstractmethod
    def bulk_remove(self,tasks:list[TaskEntity])->list[TaskEntity]:
        pass
    
    @abstractmethod
    def find_by_ids(self,ids:list[TaskId])->list[TaskEntity]:
        pass
    
    @abstractmethod
    def find_by_user(self,user_id:'user.UserId'):
        pass