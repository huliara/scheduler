from database import get_db
from ddd.infra.auth import get_current_active_user
from ddd.infra.repository import (ShiftRepository,
                                  TaskRepository, TemplateRepository,GroupRepository,UserRepository)
from ddd.service.usecases.template import (ShiftFromTemplateParams,
                                           ShiftFromTemplateUseCase)
from fastapi import APIRouter, Depends
from schemas.template import ShiftFromTemplateRequest
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return ShiftFromTemplateUseCase(TemplateRepository(db),ShiftRepository(db),TaskRepository(db),GroupRepository(db),UserRepository(db))

@router.post("/{template_id}/generate")
async def template_generate_shifts(template_id:str,request:ShiftFromTemplateRequest, 
                                  user=Depends(get_current_active_user),
                              usecase:ShiftFromTemplateUseCase=Depends(__usecase_di)):
    generated_shifts=await usecase.execute(ShiftFromTemplateParams(creater_id=user.id,
                                                    template_id=template_id,
                                                    start_date=request.start_day,
                                                    add_default_worker=request.add_default_worker))
    
    response=[shift.to_dict() for shift in generated_shifts]
    return response
    
