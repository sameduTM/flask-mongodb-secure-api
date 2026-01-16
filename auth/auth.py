from db.connectDB import db
from flask_login import UserMixin
from main import login_manager

data = db.users.find()

users = []

for user in data:
    users.append({"email": user["email"], "password": user["password"]})


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get("email")
    if email not in users:
        return
    user = User()
    user.id = email
    return user
