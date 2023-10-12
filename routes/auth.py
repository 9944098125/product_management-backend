from flask import request, Blueprint

from controllers.auth import register_user, login_user, get_all_users, delete_all_users

auth_blueprint = Blueprint("auth", __name__)


# register route
@auth_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data["name"]
    email = data["email"]
    password = data["password"]
    is_admin = data.get("is_admin")
    return register_user(name, email, password, is_admin)


# login route
@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    return login_user(email, password)


# get all users route
@auth_blueprint.route("/users", methods=["GET"])
def get_users():
    return get_all_users()


@auth_blueprint.route("/delete", methods=["DELETE"])
def delete_users():
    return delete_all_users()
