from database import SessionLocal
from ddd.infra.auth import get_password_hash
from models.models import User


def create_admin(name: str, password: str, room_number: str):
    db = SessionLocal()
    new_user = User(
        name=name,
        room_number=room_number,
        password=get_password_hash(password),
        is_admin=True,
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

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
    