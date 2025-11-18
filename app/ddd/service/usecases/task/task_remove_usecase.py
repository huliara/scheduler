from app.ddd.domain.task import ITaskRepository, TaskEntity, TaskId

from ..remove_usecase import RemoveUseCase


class TaskRemoveUseCase(RemoveUseCase[TaskId, TaskEntity, ITaskRepository]):
   pass