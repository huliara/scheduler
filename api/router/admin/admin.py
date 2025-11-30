from database import get_db
from ddd.infra.auth import get_admin_user
from fastapi import APIRouter, Depends, HTTPException, status
from models.models import GroupUser
from router.user import group_user_display
from schemas.admin import AddUserRequest, GroupPostRequest
from sqlalchemy.future import select
from sqlalchemy.orm import Session

router = APIRouter(
    dependencies=[Depends(get_admin_user)],
)


@router.post("/groups/{group_id}/adduser")
async def create_owneruser(
    group_id: str, request: AddUserRequest, db: Session = Depends(get_db)
):
    response_users = []
    for user_id in request.users:
        group_user = db.scalars(
            select(GroupUser).filter_by(user_id=user_id, group_id=group_id).limit(1)
        ).first()
        if not group_user:
            group_user = GroupUser(user_id=user_id, group_id=group_id, is_owner=True)
            db.add(group_user)
            db.commit()
            db.refresh(group_user)
            response_users.append(group_user)
            continue
        group_user.is_owner = True
        db.commit()
        db.refresh(group_user)
        response_users.append(group_user)

    return {"users": [group_user_display(user) for user in response_users]}
