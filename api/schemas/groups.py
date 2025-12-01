from uuid import UUID

from pydantic import BaseModel


class Member(BaseModel):
    id: UUID
    point: float


class GroupDisplay(BaseModel):
    id: UUID
    name: str
    users: list[Member]
    task_details: list[UUID]
    template: list[UUID]

class GroupsDisplay(BaseModel):
    groups: list[GroupDisplay]

    class Config:
        from_attributes=True