from app.ddd.domain.task import ITaskRepository, TaskEntity, TaskId

from ..remove_usecase import RemoveUseCase


class TaskDetailRemoveUseCase(RemoveUseCase[TaskId, TaskEntity, ITaskRepository]):
   pass