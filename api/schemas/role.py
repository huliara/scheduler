from typing import Literal

from pydantic import BaseModel, Field


class RoleCreate(BaseModel):
    name: str = Field(max_length=20)
    permissions: list[
        Literal[
            "add_user",
            "remove_user",
            "edit_task", 
            "edit_template",
            "edit_role",
            "change_user_role",
            "edit_slot",
            "add_slot_from_template",
            "edit_point",
        ]
    ]

    class Config:
        from_attributes = True
        
class RoleDisplay(RoleCreate):
    id: str
    
    class Config:
        from_attributes = True