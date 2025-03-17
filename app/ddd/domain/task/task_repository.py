import datetime
from abc import abstractmethod

from app.ddd.core.i_repository import IRepository
from app.ddd.domain.group import GroupId
from app.ddd.domain.task_detail import TaskDetailId
from app.ddd.domain.user import UserId
from app.models.models import Task
from app.schemas.task import TaskCreate

from .task_entity import TaskEntity
from .task_value_object import TaskId


class ITaskRepository(IRepository[TaskEntity,TaskId]):
    @abstractmethod
    def add(self,name:str,start_time:datetime.datetime,creater_id:UserId,taskdetail_id:TaskDetailId)->TaskEntity:
        pass
    
    @abstractmethod
    def save(self,task:TaskEntity)->TaskEntity:
        pass
    
    @abstractmethod
    def find_all(self,group_id:GroupId,end:bool|None)->list[TaskEntity]:
        pass

    @abstractmethod
    def refresh_to_entity(self, model: Task) -> TaskEntity:
        pass
    
    @abstractmethod
    def bulk_add(self,tasks:list[TaskEntity])->list[TaskEntity]:
        pass
    
    @abstractmethod
    def bulk_remove(self,tasks:list[TaskEntity])->list[TaskEntity]:
        pass
    
    @abstractmethod
    def find_by_ids(self,group_id:GroupId,ids:list[TaskId])->list[TaskEntity]:
        pass
    
