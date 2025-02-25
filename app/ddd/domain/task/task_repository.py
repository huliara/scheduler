from abc import abstractmethod

from app.ddd.core.i_repository import IRepository
from app.models.models import Task

from .task_entity import TaskEntity
from .task_value_object import TaskId


class ITaskRepository(IRepository[TaskEntity,TaskId]):

    @abstractmethod
    def refresh_to_entity(self, model: Task) -> TaskEntity:
        pass
    
    @abstractmethod
    def bulk_add(self,tasks:list[TaskEntity])->list[TaskEntity]:
        pass