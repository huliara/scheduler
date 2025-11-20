from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.domain.user import UserEntity
from app.ddd.infra.auth import get_current_active_user
from app.ddd.infra.repository import ShiftRepository
from app.ddd.service.usecases.shift import ShiftGetAllUseCase
from app.schemas.shift import ShiftList

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return ShiftGetAllUseCase(ShiftRepository(db))



@router.get("/", response_model=ShiftList)
async def shift_getall(group_id:str|None=None,end:bool|None=None,
                      user:UserEntity=Depends(get_current_active_user),
                      usecase:ShiftGetAllUseCase=Depends(__usecase_di)):
    shifts=usecase.execute(user,group_id,end)
    response=[task.to_dict() for task in shifts]
    return {"tasks":response}
    
