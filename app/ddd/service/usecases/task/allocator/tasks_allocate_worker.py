from mip import BINARY, Model, minimize, xsum
from sqlalchemy.orm import Session

from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.task import ITaskRepository, TaskEntity
from app.ddd.domain.user import IUserRepository, UserEntity


class TasksAllocationWorkerUseCase(TransactionUseCaseBase):
    def __init__(self, db:Session):
        super().__init__(db)
        
    async def execute(self, tasks:list[TaskEntity],users:list[UserEntity])->list[TaskEntity]:
        if len(tasks)==0:
            return []
        if len(users)==0:
            return []
        if len(tasks)>40:
            raise ValueError("task_ids must be less than 40")
        if len(users)>500:
            raise ValueError("user_ids must be less than 500")
        
        result=await self.shift_calculate(users,tasks)
        
        return result
    def _transaction(self, task_ids:list[TaskEntity],user_ids:list[UserEntity])->list[TaskEntity]:
        pass
    
    #experimental
    async def shift_calculate(users:list[UserEntity],tasks:list[TaskEntity])->list[TaskEntity]:
        m=Model()
        Var=m.add_var_tensor((len(tasks),len(users)),var_type=BINARY)
        tasks=[task for task in tasks if len(task.workers)>0]
        tasks=tasks.sort(key=lambda x:x.start_time)
        
        C_more_than_min_worker=10
        C_less_than_max_woker=10
        C_more_expert_than_need=10
        C_add_new_worker=10
        C_point_equality=10
        
        x_min=m.add_var_tensor((len(tasks),))
        x_max=m.add_var_tensor((len(tasks),))
        x_exp=m.add_var_tensor((len(tasks),))
        x_new=m.add_var_tensor((len(tasks),))
        x_point=m.add_var()
        
        m.objective=minimize(xsum(C_more_than_min_worker*x_min[i]
                                  +C_less_than_max_woker*x_max[i]
                                  +C_more_expert_than_need*x_exp[i]
                                  +C_add_new_worker*x_new[i] for i in range(len(tasks)))
                             +C_point_equality*x_point)
        
        expert_metrics=[[0 for i in range(len(users))] for j in range(len(tasks))]
        for i in range(len(tasks)):
            for j in range(len(users)):
                user=users[j]
                if tasks[i].taskdetail in user.exp_tasks:
                    expert_metrics[i][j]=1
        
        slot_info_metrics=[[task.taskdetail.min_worker,
                            task.taskdetail.max_worker,
                            task.taskdetail.exp_worker,
                            task.taskdetail.wage] for task in tasks]

        for i in range(len(tasks)):
            m+=xsum(Var[i,j] for j in range(len(users)))+x_min[i]>=slot_info_metrics[i][0]
            m+=xsum(Var[i,j] for j in range(len(users)))-x_max[i]<=slot_info_metrics[i][1]
            m+=xsum(Var[i,j]*expert_metrics[i][j] for j in range(len(users)))+x_exp[i]>=slot_info_metrics[i][2]
            m+=xsum(Var[i,j]*(1-expert_metrics[i][j]) for j in range(len(users)))+x_new[i]>=slot_info_metrics[i][1]-slot_info_metrics[i][2]
        
        for j in range(len(users)):
            m+=xsum(Var[i,j]*slot_info_metrics[i][3] for i in range(len(tasks)))+user[j].point<=x_point

        m.optimize()
        
        result=[[Var[i,j].x for j in range(len(users))] for i in range(len(tasks))]
        for i in range(len(tasks)):
            for j in range(len(users)):
                if result[i][j]==1:
                    try:
                        tasks[i].add(users[j])
                    except:
                        pass
        return tasks
    