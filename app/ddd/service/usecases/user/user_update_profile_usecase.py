from dataclasses import dataclass

from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.task_detail import ITaskDetailRepository, TaskDetailId
from app.ddd.domain.user import IUserRepository, UserEntity


@dataclass
class UserUpdateParams:
    def __init__(self,id:int,name:str,room_number:str,exp_tasks:list[TaskDetailId]):
        self.id=id
        self.name=name
        self.room_number=room_number
        self.exp_tasks=exp_tasks

class UserUpdateUseCase(TransactionUseCaseBase):
    def __init__(self, db,user_repository:IUserRepository,taskdetail_repository:ITaskDetailRepository):
        super().__init__(db)
        self.user_repository=user_repository
        self.taskdetail_repository=taskdetail_repository
    
    def execute(self,params:type[UserUpdateParams])->UserEntity:
        return self._transaction(params)

    def _transaction(self, params:type[UserUpdateParams])->UserEntity:
        try:
            target_user=self.user_repository.find_by_id(params.id)
        except:
            raise UseCaseException(f'user_id:{params.id} not found')
        try:
            _=self.taskdetail_repository.find_by_ids([taskdetail for taskdetail in params.exp_tasks])
        except:
            raise UseCaseException('Invalid exp_task found')
        
        target_user.update_profile({
            'name':params.name,
            'room_number':params.room_number,
            'exp_tasks':params.exp_tasks
        })
        
        try:
            user=self.user_repository.save(target_user)
        except:
            raise UseCaseException(f'invalid enitity:{target_user}')
        return user