from conftest import client

from app.cruds.auth import verify_password
from app.cruds.admin import create_admin

user = {
    "name": "testUser",
    "password": "testUserPassword",
    "room_number": "B310",
}


def test_create_user():
    response = create_admin(user["name"], user["password"], user["room_number"])
    assert response.name == "testUser"
    assert response.room_number == "B310"
    assert verify_password(user["password"], response.password)
    assert response.is_admin
    assert response.is_active

    response_user = client.post(
        "/login", data={"username": "testUser", "password": "testUserPassword"}
    )
    access_token = response_user.json().get("access_token")
    print("access_token", response_user.json())
    assert response_user.status_code == 200
    assert access_token
    assert response_user.json().get("id")
    assert response_user.json().get("name") == "testUser"
    assert response_user.json().get("token_type") == "bearer"

    response_get = client.get(
        "/admin/users/" + response_user.json().get("id"),
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response_get.status_code == 200
    assert response_get.json().get("name") == "testUser"
    assert response_get.json().get("room_number") == "B310"

    response_group = client.post(
        "/admin/groups",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"name": "testGroup"},
                )
    assert response_group.status_code == 200
    assert response_group.json().get("name") == "testGroup"
    response_group_get = client.get(
        "/admin/groups/" + response_group.json().get("id"),
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response_group_get.status_code == 200
    assert response_group_get.json().get("name") == "testGroup"
    response_user2 = client.post(
        "/admin/users",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": "testUser2",
            "room_number": "B311",
            "password": "superUserPassword",
            "is_admin": False,
        },
    )
    assert response_user2.status_code == 200
    assert response_user2.json().get("name") == "testUser2"
    assert response_user2.json().get("room_number") == "B311"
    assert not response_user2.json().get("is_admin")
    response_user_get = client.get(
        "/admin/users/" + response_user2.json().get("id"),
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response_user_get.status_code == 200
    assert response_user_get.json().get("name") == "testUser2"
    assert response_user_get.json().get("room_number") == "B311"
    assert not response_user_get.json().get("is_admin")
    response = client.post(
        "/admin/groups/" + response_group.json().get("id") + "/adduser",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"users": [response_user2.json().get("id")]},
    )
    assert response.status_code == 200
    assert response.json().get("users")[0].get("name") == "testUser2"
    assert response.json().get("users")[0].get("role") == "super"
    super_user_login = client.post(
        "/login", data={"username": "testUser2", "password": "superUserPassword"}
    )
    assert super_user_login.status_code == 200
    super_user_token = super_user_login.json().get("access_token")
    assert super_user_token
    assert super_user_login.json().get("id")
    assert super_user_login.json().get("name") == "testUser2"
    assert super_user_login.json().get("token_type") == "bearer"
    fail_create_group = client.post(
        "/admin/groups",
        headers={"Authorization": f"Bearer {super_user_token}"},
        json={"name": "testGroup2"},
    )
    assert fail_create_group.status_code == 403
    fail_create_user = client.post(
        "/admin/users",
        headers={"Authorization": f"Bearer {super_user_token}"},
        json={"name": "testUser3", "room_number": "B312", "is_admin": True},
    )
    assert fail_create_user.status_code == 403
    fail_user_add=client.post(
        "/admin/groups/" + response_group.json().get("id") + "/adduser",
        headers={"Authorization": f"Bearer {super_user_token}"},
        json={"users": [response_user.json().get("id")]},
    )
    assert fail_user_add.status_code == 403
