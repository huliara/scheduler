from ddd.domain.task.task_value_object import TaskId
from ddd.domain.task.task_entity import TaskEntity
from ddd.domain.task.task_repository import ITaskRepository 

from ..remove_usecase import RemoveUseCase


class TaskRemoveUseCase(RemoveUseCase[TaskId, TaskEntity, ITaskRepository]):
   pass