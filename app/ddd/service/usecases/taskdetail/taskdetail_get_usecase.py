
from app.ddd.domain.task_detail import (ITaskDetailRepository,
                                        TaskDetailEntity, TaskDetailId)

from ..get_usecase import GetUseCase


class TaskDetailGetUseCase(GetUseCase[TaskDetailId,TaskDetailEntity,ITaskDetailRepository]):
    pass