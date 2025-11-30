from ddd.domain.task import ITaskRepository, TaskEntity
from ddd.service.usecases.getall_usecase import GetAllUseCase


class TaskGetAllUseCase(GetAllUseCase[TaskEntity,ITaskRepository]):
    pass