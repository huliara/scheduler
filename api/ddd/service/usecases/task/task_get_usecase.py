
from ddd.domain.task import ITaskRepository, TaskEntity, TaskId

from ..get_usecase import GetUseCase


class TaskGetUseCase(GetUseCase[TaskId,TaskEntity,ITaskRepository]):
    pass