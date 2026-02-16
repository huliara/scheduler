import os
import sys

# プロジェクトルートディレクトリ(apiディレクトリ)をパスに追加
current_dir = os.path.dirname(os.path.abspath(__file__))
api_dir = os.path.dirname(current_dir)
sys.path.append(api_dir)

from database import SessionLocal
from ddd.infra.repository.user_repository import UserRepository
from ddd.domain.user.user_entity import UserEntity


def create_admin(name: str, password: str, room_number: str):
    db = SessionLocal()
    user_repo = UserRepository(db)
    
    try:
        new_user_entity = UserEntity(
            id=None,
            name=name,
            room_number=room_number,
            exp_tasks=[],
            is_admin=True,
            is_active=True,
        )
        # Repository handles hashing
        created_user = user_repo.add(new_user_entity, password)
        return created_user
    finally:
        db.close()


def createadminuser():
    name=input("Enter name: ")
    password=input("Enter password: ")
    re_password=input("Re-enter password: ")
    room_number=input("Enter room number: ")
    if password!=re_password:
        print("Passwords do not match")
        return
    response = create_admin(name, password, room_number)
    print(response)

if __name__ == "__main__":
    createadminuser()
    