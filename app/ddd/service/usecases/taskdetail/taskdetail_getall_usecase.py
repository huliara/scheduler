from app.ddd.domain.task import ITaskRepository, TaskEntity
from app.ddd.service.usecases.getall_usecase import GetAllUseCase


class TaskDetailGetAllUseCase(GetAllUseCase[TaskEntity,ITaskRepository]):
    pass