from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.cruds.auth import get_current_active_user
from app.database import get_db
from app.ddd.infra.repository import (GroupRepository, TaskDetailRepository,
                                      TaskRepository, TemplateRepository)
from app.ddd.service.usecases.task import TaskAllocationByGroup
from app.ddd.service.usecases.template import (TaskFromTemplateParams,
                                               TaskFromTemplateUseCase)
from app.schemas.template import TaskFromTemplate

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TaskFromTemplateUseCase(db,TemplateRepository(db),TaskRepository(db),TaskDetailRepository(db))

def __usecase_di_2(db:Session=Depends(get_db)):
    return TaskAllocationByGroup(db,TaskRepository(db),GroupRepository(db))

@router.post("/{template_id}/generate")
async def template_generate_tasks(group_id: str,template_id:str,request:TaskFromTemplate, 
                                  user=Depends(get_current_active_user),
                              usecase:TaskFromTemplateUseCase=Depends(__usecase_di),
                              usecase2:TaskAllocationByGroup=Depends(__usecase_di_2)):
    generated_tasks=usecase.execute(TaskFromTemplateParams(creater_id=user.id,
                                                    template_id=template_id,
                                                    start_date=request.start_day))
    if request.add_default_worker:
        generated_tasks=await usecase2.execute([task.id for task in generated_tasks],group_id)
    response=[task.to_dict() for task in generated_tasks]
    return response
    
