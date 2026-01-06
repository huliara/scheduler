
from ddd.domain.task.task_value_object import TaskId
from ddd.domain.task.task_entity import TaskEntity
from ddd.domain.task.task_repository import ITaskRepository 

from ..get_usecase import GetUseCase


class TaskGetUseCase(GetUseCase[TaskId,TaskEntity,ITaskRepository]):
    pass