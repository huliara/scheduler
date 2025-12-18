from uuid import UUID

from pydantic import BaseModel


class Member(BaseModel):
    id: UUID
    point: float


class GroupDisplay(BaseModel):
    id: UUID
    name: str
    users: list[Member]
    task: list[UUID]
    template: list[UUID]



    class Config:
        from_attributes=True