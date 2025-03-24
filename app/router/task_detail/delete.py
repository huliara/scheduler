from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import TaskDetailRepository
from app.ddd.service.usecases.taskdetail import TaskDetailRemoveUseCase
from app.schemas.taskdetail import TaskDetailDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TaskDetailRemoveUseCase(db,TaskDetailRepository(db))


@router.delete("/{detail_id}", response_model=TaskDetailDisplay)
async def taskdetail_delete(group_id: str,detail_id:str,
                            usecase:TaskDetailRemoveUseCase=Depends(__usecase_di)):
    response=usecase.execute(detail_id).to_dict()
    return response
    
