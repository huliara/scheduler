import ddd.infra.message as message
from database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/today")
async def today_slots(db: Session = Depends(get_db)):
    message.today_slots(db)
    return
