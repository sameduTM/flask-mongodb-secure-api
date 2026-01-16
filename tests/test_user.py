import requests
from views import index
# from api import user

EMAIL = "jane@doe.com"
PASSWORD = "janedoe1234"


def test_index():
    assert index.index() == {"status": "OK"}


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
