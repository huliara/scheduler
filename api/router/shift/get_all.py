from database import get_db
from ddd.domain.user import UserEntity
from ddd.infra.auth import get_current_active_user
from ddd.infra.repository import ShiftRepository
from ddd.service.usecases.shift import ShiftGetAllUseCase
from fastapi import APIRouter, Depends
from schemas.shift import ShiftList
from sqlalchemy.orm import Session

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
    
