from database import get_db
from ddd.domain.user.user_entity import UserEntity
from ddd.infra.auth import get_current_active_user
from ddd.infra.repository import ShiftRepository
from ddd.service.usecases.shift import ShiftGetUserRelevantUseCase
from fastapi import APIRouter, Depends
from schemas.shift import ShiftDisplay
from sqlalchemy.orm import Session

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return ShiftGetUserRelevantUseCase(ShiftRepository(db))



@router.get("/shifts", response_model=list[ShiftDisplay])
async def get_shifts_relevant_user(user:UserEntity=Depends(get_current_active_user),
                                 usecase:ShiftGetUserRelevantUseCase=Depends(__usecase_di)):
    shifts=usecase.execute(user.id)

    return [shift.to_dict() for shift in shifts]
    
