
from app.ddd.domain.task import ITaskRepository, TaskEntity, TaskId

from ..get_usecase import GetUseCase


class TaskDetailGetUseCase(GetUseCase[TaskId,TaskEntity,ITaskRepository]):
    pass