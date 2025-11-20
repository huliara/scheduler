from datetime import datetime, timedelta, timezone
from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.ddd.domain.user import UserEntity
from app.models.models import GroupUser, User

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "9343174155ee7db2d9ad9985aac201fec735c0a56a298e0ad4296e9ea91c2243"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class TokenData(BaseModel):
    username: Union[str, None] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str):
    user = db.scalars(select(User).filter_by(name=username).limit(1)).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return UserEntity.from_model(user)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_402_PAYMENT_REQUIRED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.scalars(select(User).filter_by(name=token_data.username).limit(1)).first()
    if user is None:
        raise credentials_exception
    return UserEntity.from_model(user)


async def get_current_active_user(current_user: UserEntity = Depends(get_current_user)):
    if current_user.is_active:
        return current_user
    raise HTTPException(status_code=400, detail="Inactive user")


async def get_admin_user(current_user: UserEntity = Depends(get_current_user)):
    if current_user.is_admin and current_user.is_active:
        return current_user
    raise HTTPException(status_code=403, detail="Not admin user")


def check_privilege(group_id: str, user_id: str, permission: str, db: Session):
    group_user = db.scalars(
        select(GroupUser).filter_by(group_id=group_id, user_id=user_id).limit(1)
    ).first()
    user = db.get(User, user_id)

    if user.is_admin:
        return

    if not group_user:
        raise HTTPException(status_code=403, detail="このグループには所属していません")

    if permission == "normal":
        return

    if group_user.is_owner:
        return

    for role in group_user.roles:
        if getattr(role, permission):
            return

    raise HTTPException(status_code=403, detail="権限がありません")
