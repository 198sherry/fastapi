from app import schemas 
#from .database import client, session
import pytest
from jose import jwt
from app.config import settings
#from .conftest import test_user, client, session

# @pytest.fixture
# def test_user(client):
#     user_data = {"email":"email1@gmail.com", "password":"password1"}
#     res = client.post("/users/", json=user_data)
#     new_user = res.json()
#     new_user['password'] = user_data['password']

#     assert res.status_code == 201
#     return new_user

# def test_root(client):
#     res = client.get("/")
#     print(res.json().get("message"))
#     assert res.json().get("message") == "Welcome to my world"
#     assert res.status_code == 200

# def test_create_user():
#     res = client.post(
#         "/users/", json={"email":"email5@gmail.com", "password":"password123"})
#     print(res.json())
#     new_user = schemas.UserOut(**res.json())
#     assert new_user.email == "email5@gmail.com"
#     assert res.status_code == 201


def test_create_user(client):
    res = client.post(
        "/users/", json={"email":"email5@gmail.com", "password":"password123"})
    print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "email5@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username":test_user['email'], "password":test_user['password']})
    login_res = schemas.Token(**res.json())

    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms = [settings.algorithm])
    id= payload.get("user_id")

    assert id ==test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('email3@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('email2@gmail.com', None, 422)])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username":email, "password":password})

    assert res.status_code == status_code
    #assert res.json().get("detail") == "Invalid password"
