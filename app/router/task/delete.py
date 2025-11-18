from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.infra.repository import TaskRepository
from app.ddd.service.usecases.task import TaskRemoveUseCase
from app.schemas.taskdetail import TaskDetailDisplay

router = APIRouter()

def __usecase_di(db:Session=Depends(get_db)):
    return TaskRemoveUseCase(db,TaskRepository(db))


@router.delete("/{detail_id}", response_model=TaskDetailDisplay)
async def taskdetail_delete(group_id: str,detail_id:str,
                            usecase:TaskRemoveUseCase=Depends(__usecase_di)):
    response=usecase.execute(detail_id).to_dict()
    return response
    
