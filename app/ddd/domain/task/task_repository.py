from abc import abstractmethod

import app.models.models as models
from app.ddd.core.i_repository import IRepository

from .task_value_object import TaskId
from .task_entity import TaskEntity


class ITaskRepository(IRepository[TaskEntity,TaskId]):
    
    @abstractmethod
    def _refresh_to_entity(self, model: "models.Task") -> TaskEntity:
        pass
    
    @abstractmethod
    def find_by_ids(self, ids: list[TaskId]) -> list[TaskEntity]:
        pass
    