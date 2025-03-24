from app.ddd.domain.task_detail import ITaskDetailRepository, TaskDetailEntity
from app.ddd.service.usecases.getall_usecase import GetAllUseCase


class TaskDetailGetAllUseCase(GetAllUseCase[TaskDetailEntity,ITaskDetailRepository]):
    pass