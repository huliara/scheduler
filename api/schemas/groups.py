from uuid import UUID

from pydantic import BaseModel


class Member(BaseModel):
    name:str
    user_id: UUID
    group_id: UUID
    point: float
    is_active: bool

class GroupDisplay(BaseModel):
    id: UUID
    name: str
    users: list[Member]
    task: list[UUID]
    template: list[UUID]



    class Config:
        from_attributes=True