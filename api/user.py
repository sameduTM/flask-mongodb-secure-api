import bcrypt

from bson import ObjectId
from config import jwt
from db.connectDB import connect  # noqa
from flask import Blueprint, request, jsonify
from models.user import User

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required

user_bp = Blueprint("user_bp", __name__, url_prefix="/api")

data = User.objects

users = []

for user in data:
    users.append(
        {"email": user.email, "name": user.name, "posted": user.posted})


def hash_password(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def check_password(password, stored_hashed):
    return bcrypt.checkpw(password, stored_hashed)


@jwt.user_identity_loader
def user_identity_lookup(user):
    user_id = str(user['_id'])
    return user_id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return db.users.find_one({"_id": ObjectId(identity)})


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    data = request.authorization
    creds = data.parameters
    email = creds.get('username')
    password = creds.get('password')
    user = db.users.find_one({"email": email})
    if user and user["password"] == password:
        access_token = create_access_token(identity=user)
        headers = {"Authorization": f"Bearer {access_token}"}
        return jsonify({"Status": "Login Successful"}), 200, headers
    return {"Status": "Login failed"}, 401


@user_bp.route("/all_users", methods=["GET"])
# @jwt_required()
def get_all_users():
    return jsonify(users)


@user_bp.route("/create_user", methods=["GET", "POST"])
# @jwt_required()
def create_user():
    try:
        data = request.get_json()
        name, email, password = data.values()
        hashed_password = hash_password(password)
        user = User(name=name, email=email, password=hashed_password)
        user.save()
        return jsonify(
            {
                "Status": "User added successfully!"
            }
        )
    except Exception as e:
        print("Error:", e)
        return {"Error": "Could not create user"}


@user_bp.route("/update_user/<user_id>", methods=["GET", "PUT"])
@jwt_required()
def update_user(user_id):
    try:
        data = request.get_json()
        db.users.find_one_and_update(
            {"_id": ObjectId(user_id)}, {"$set": data})
        return {"Status": "User updated successfully"}
    except Exception as e:
        print("Error:", e)
        return {"Status": "Error updating user"}


@user_bp.route("/delete_user/<user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    try:
        user = db.users.find_one_and_delete({"_id": ObjectId(user_id)})
        return {"user_id": user["name"]}
    except Exception as e:
        print("Error:", e)
        return {"Status": "Error deleting user"}
