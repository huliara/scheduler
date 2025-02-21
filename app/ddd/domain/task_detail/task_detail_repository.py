from abc import abstractmethod

from app.ddd.core.i_repository import IRepository
from app.models.models import TaskDetail

from .task_detail_entity import TaskDetailEntity
from .task_detail_value_object import TaskDetailId


class ITaskDetailRepository(IRepository[TaskDetailEntity,TaskDetailId]):
    
    @abstractmethod
    def _refresh_to_entity(self, model: TaskDetail) -> TaskDetailEntity:
        pass