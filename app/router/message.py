from fastapi import APIRouter, Depends
from app.database import get_db
from sqlalchemy.orm import Session
import app.ddd.infra.message as message

router = APIRouter()


@router.post("/today")
async def today_slots(db: Session = Depends(get_db)):
    message.today_slots(db)
    return
