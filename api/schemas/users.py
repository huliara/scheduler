from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    room_number: str

class UserUpdatePassword(BaseModel):
    password: str

class UserCreate(UserBase):
    password: str
    exp_tasks: list[UUID]


class UserUpdate(UserBase):
    exp_task: list[UUID]


class AdminUserCreate(UserBase):
    password: str
    is_admin: bool

    class Config:
        orm_mode = True


class AdminUserPatch(UserBase):
    exp_task: list[UUID]
    point: int


class UserDisplay(UserBase):
    id: UUID
    point: float
    is_active: bool
    exp_tasks: list[UUID]
    shifts: list[UUID]

class UsersDisplay(BaseModel):
    users: list[UserDisplay]



class AdminUserDisplay(UserBase):
    id: UUID
    is_admin: bool


class Role(BaseModel):
    id: UUID
    name: str


class MemberDisplay(BaseModel):
    id: UUID
    point: float
    user_id: UUID
    group_id: UUID


class GroupUsers(BaseModel):
    users: list[MemberDisplay]


class UserAddRequest(BaseModel):
    user_id: str


class UsersAddRequest(BaseModel):
    user_ids: list[str]


class UserRolesChange(BaseModel):
    role_ids: list[str]
