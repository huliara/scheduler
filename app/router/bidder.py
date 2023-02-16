from fastapi import APIRouter,Depends,HTTPException,status
from app.schemas.bid import BidRequest,TenderRequest
from app.models.users import User
from app.models.bid import Bid
from sqlalchemy.orm import Session
from app.database import get_db
from app.cruds.auth import get_current_active_user
import app.cruds.bidder as crud
router=APIRouter()

@router.get("/")
async def bid_get(bid_id:str|None=None,user_id:str|None=None,db:Session=Depends(get_db)):
    bidder=crud.bidder_get(bid_id,user_id,db)
    return bidder
    