from abc import abstractmethod

import app.models.models as models
from app.ddd.core.i_repository import IRepository

from .task_detail_entity import TaskDetailEntity
from .task_detail_value_object import TaskDetailId


class ITaskDetailRepository(IRepository[TaskDetailEntity,TaskDetailId]):
    
    @abstractmethod
    def _refresh_to_entity(self, model: "models.TaskDetail") -> TaskDetailEntity:
        pass
    
    @abstractmethod
    def find_by_ids(self, ids: list[TaskDetailId]) -> list[TaskDetailEntity]:
        pass
    