from abc import abstractmethod

import models.models as models
from ddd.core.i_repository import IRepository

from .task_entity import TaskEntity
from .task_value_object import TaskId


class ITaskRepository(IRepository[TaskEntity,TaskId]):
    
    @abstractmethod
    def _refresh_to_entity(self, model: "models.Task") -> TaskEntity:
        pass
    
    @abstractmethod
    def find_by_ids(self, ids: list[TaskId]) -> list[TaskEntity]:
        pass
    