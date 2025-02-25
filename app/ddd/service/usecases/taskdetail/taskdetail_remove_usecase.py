from app.ddd.domain.task_detail import (ITaskDetailRepository,
                                        TaskDetailEntity, TaskDetailId)

from ..remove_usecase import RemoveUseCase


class TaskDetailRemoveUseCase(RemoveUseCase[TaskDetailId, TaskDetailEntity, ITaskDetailRepository]):
   pass