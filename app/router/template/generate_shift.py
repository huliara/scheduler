from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.auth import get_current_active_user
from app.ddd.infra.repository import (GroupRepository, ShiftRepository,
                                      TaskRepository, TemplateRepository)
from app.ddd.service.usecases.shift import ShiftAllocationByGroup
from app.ddd.service.usecases.template import (ShiftFromTemplateParams,
                                               ShiftFromTemplateUseCase)
from app.schemas.template import TaskFromTemplate

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return ShiftFromTemplateUseCase(TemplateRepository(db),ShiftRepository(db),TaskRepository(db))

def __usecase_di_2(db:Session=Depends(get_db)):
    return ShiftAllocationByGroup(ShiftRepository(db),GroupRepository(db))

@router.post("/{template_id}/generate")
async def template_generate_shifts(template_id:str,request:TaskFromTemplate, 
                                  user=Depends(get_current_active_user),
                              usecase:ShiftFromTemplateUseCase=Depends(__usecase_di),
                              usecase2:ShiftAllocationByGroup=Depends(__usecase_di_2)):
    generated_shifts=usecase.execute(ShiftFromTemplateParams(creater_id=user.id,
                                                    template_id=template_id,
                                                    start_date=request.start_day))
    if request.add_default_worker:
        if not request.group_id:
            raise ValueError("group_id is required when add_default_worker is True")
        generated_shifts=await usecase2.execute([task.id for task in generated_shifts],request.group_id)
    response=[task.to_dict() for task in generated_shifts]
    return response
    
