from dataclasses import dataclass, field

from mip import BINARY, Model, minimize, xsum

from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.shift import IShiftRepository, ShiftEntity
from app.ddd.domain.task import TaskId
from app.ddd.domain.user import IUserRepository, UserId


@dataclass
class AllocWorkerDTO:
    id:UserId
    point:int
    exp_tasks:list[TaskId]=field(default_factory=list)


class ShiftAllocationWorkerUseCase(TransactionUseCaseBase):
    def __init__(self,user_repository:IUserRepository,shift_repository:IShiftRepository):
        self.user_repository=user_repository
        self.shift_repository=shift_repository
    async def execute(self, shifts:list[ShiftEntity],users:list[AllocWorkerDTO])->list[ShiftEntity]:
        if len(shifts)==0:
            return []
        if len(users)==0:
            return []
        if len(shifts)>40:
            raise ValueError("shift_ids must be less than 40")
        if len(users)>500:
            raise ValueError("user_ids must be less than 500")
        
        result=await self.shift_calculate(users,shifts,self.user_repository)
        response=[]
        for shift in result:
            shift=self.shift_repository.save(shift)
            response.append(shift)
            
        return response
    def _transaction(self)->list[ShiftEntity]:
        pass
    
    #experimental
    async def shift_calculate(users:list[AllocWorkerDTO],shifts:list[ShiftEntity],
                              user_repository:IUserRepository)->list[ShiftEntity]:
        m=Model()
        Var=m.add_var_tensor((len(shifts),len(users)),var_type=BINARY)
        shifts=[shift for shift in shifts if len(shift.workers)>0]
        shifts=shifts.sort(key=lambda x:x.start_time)
        
        C_more_than_min_worker=10
        C_less_than_max_woker=10
        C_more_expert_than_need=10
        C_add_new_worker=10
        C_point_equality=10
        
        x_min=m.add_var_tensor((len(shifts),))
        x_max=m.add_var_tensor((len(shifts),))
        x_exp=m.add_var_tensor((len(shifts),))
        x_new=m.add_var_tensor((len(shifts),))
        x_maxpoint=m.add_var()
        
        m.objective=minimize(xsum(C_more_than_min_worker*x_min[i]
                                  +C_less_than_max_woker*x_max[i]
                                  +C_more_expert_than_need*x_exp[i]
                                  +C_add_new_worker*x_new[i] for i in range(len(shifts)))
                                  +C_point_equality*x_maxpoint)
        
        expert_metrics=[[0 for i in range(len(users))] for j in range(len(shifts))]
        for i in range(len(shifts)):
            for j in range(len(users)):
                user=users[j]
                if shifts[i].task in user.exp_tasks:
                    expert_metrics[i][j]=1
        
        slot_info_metrics=[[shift.task.min_worker,
                            shift.task.max_worker,
                            shift.task.exp_worker,
                            shift.task.wage] for shift in shifts]

        for i in range(len(shifts)):
            m+=xsum(Var[i,j] for j in range(len(users)))+x_min[i]>=slot_info_metrics[i][0]
            m+=xsum(Var[i,j] for j in range(len(users)))-x_max[i]<=slot_info_metrics[i][1]
            m+=xsum(Var[i,j]*expert_metrics[i][j] for j in range(len(users)))+x_exp[i]>=slot_info_metrics[i][2]
            m+=xsum(Var[i,j]*(1-expert_metrics[i][j]) for j in range(len(users)))+x_new[i]>=slot_info_metrics[i][1]-slot_info_metrics[i][2]
        
        for j in range(len(users)):
            m+=xsum(Var[i,j]*slot_info_metrics[i][3] for i in range(len(shifts)))+users[j].point<=x_maxpoint

        m.optimize()
        
        result=[[Var[i,j].x for j in range(len(users))] for i in range(len(shifts))]
        for i in range(len(shifts)):
            for j in range(len(users)):
                if result[i][j]==1:
                    try:
                        user_entity=user_repository.find_by_id(users[j].id)
                        shifts[i].add(user_entity)
                    except:
                        pass
        return shifts
    