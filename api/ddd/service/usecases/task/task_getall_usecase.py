from ddd.domain.task.task_entity import TaskEntity
from ddd.domain.task.task_repository import ITaskRepository 
from ddd.service.usecases.getall_usecase import GetAllUseCase


class TaskGetAllUseCase(GetAllUseCase[TaskEntity,ITaskRepository]):
    pass