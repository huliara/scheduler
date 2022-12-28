from typing import List, Optional,TYPE_CHECKING
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
if TYPE_CHECKING:
    from schemas.users import User

class AchivementBase(BaseModel):
    term:int
    name:str
    
class Achivement(BaseModel):
    id:UUID
    user:List["User"]
    class Config:
        orm_mode=True
    