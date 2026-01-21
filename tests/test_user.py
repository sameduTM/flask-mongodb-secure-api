import os
import requests
from db.connectDB import connect  # noqa
from dotenv import load_dotenv
from models.user import User

load_dotenv()

EMAIL = os.getenv("PYTEST_EMAIL")
PASSWORD = os.getenv("PYTEST_PASSWORD")


def get_token():
    url = "http://127.0.0.1:5000/api/login"
    response = requests.get(url, auth=(EMAIL, PASSWORD))
    token = response.headers.get('Authorization').replace("Bearer ", "")
    return token


TOKEN = get_token()


def test_index():
    url = "http://127.0.0.1:5000/"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == {"Status": "OK"}


def test_login():
    url = "http://127.0.0.1:5000/api/login"
    response = requests.get(url, auth=(EMAIL, PASSWORD))
    assert response.status_code == 200
    assert response.json() == {"Status": "Login Successful"}


def test_wrong_login():
    url = "http://127.0.0.1:5000/api/login"
    response = requests.get(url, auth=("EMAIL", "PASSWORD"))
    assert response.status_code == 401
    assert response.json() == {"Status": "Login failed"}


def test_create_user():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    payload = {"name": "Jessica Jones", "email": "jessica@jones.com",
               "password": "jessjones@1234"}
    response = requests.post(
        "http://127.0.0.1:5000/api/create_user", headers=headers, json=payload)
    assert response.status_code == 201
    assert response.json() == {"Status": "User added successfully!"}


def test_get_all_users():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(
        "http://127.0.0.1:5000/api/all_users", headers=headers)
    assert response.status_code == 200


def get_user_id():
    user = User.objects(email="john@doe.com").first()
    USER_ID = user.id.__str__()
    return USER_ID


USER_ID = get_user_id()


def test_update_user():
    url = f"http://127.0.0.1:5000/api/update_user/{USER_ID}"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    payload = {"priv": "admin"}
    response = requests.put(url, headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json() == {"Status": "User updated successfully"}


def test_delete_user():
    url = f"http://127.0.0.1:5000/api/delete_user/{USER_ID}"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.delete(url, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"Status": "User removed successfully"}
