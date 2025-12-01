from pydantic import BaseModel


class GroupPostRequest(BaseModel):
    name: str

    class Config:
        from_attributes = True


class AddUserRequest(BaseModel):
    user_ids: list[str]

    class Config:
        from_attributes = True
