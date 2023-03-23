from flask import Blueprint, request, jsonify

from db.queries import UserQueries
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    current_user,
)
from psycopg2 import DatabaseError
from dependency_injector.wiring import Provide, inject

from container import Container
from . import auth


@auth.route("/login", methods=["POST"])
@inject
def login(
    users: UserQueries = Provide[Container.user_queries]
):
    body = request.json
    email = body["email"]
    password = body["password"]
    errors = []
    if email is None or not isinstance(email, str):
        errors.append("'email' is a required string")
    if password is None or not isinstance(password, str):
        errors.append("'password' is a required string")
    if len(errors) > 0:
        return (jsonify({"errors": errors}), 400)

    try:
        if (
            user := users.get_user_by_email_and_password(email, password)
        ) is not None:
            return (
                jsonify(
                    {
                        "jwt": create_access_token(identity=user),
                        "refresh": create_refresh_token(identity=user),
                    }
                ),
                200,
            )
        else:
            return (
                jsonify({"error": "no user exists matching that email and password"}),
                400,
            )
    except (Exception, DatabaseError) as err:
        return (jsonify({"error": err}), 500)


@auth.route("/register", methods=["POST"])
@inject
def register(
    users: UserQueries = Provide[Container.user_queries]
):
    if current_user:
        return (jsonify({"error": "logged in users cannot create users"}), 400)
    body = request.json
    email = body["email"]
    password = body["password"]
    username = body["username"]
    display_name = body["displayName"]
    errors = []
    if email is None:
        errors.append("'email' is a required string")
    if password is None or not isinstance(password, str):
        errors.append("'password' is a required string")
    if username is None or not isinstance(username, str):
        errors.append("'username' is a required string")
    if display_name is None or not isinstance(display_name, str):
        errors.append("'display_name' is a required string")
    if len(errors) > 0:
        return (jsonify({"errors": errors}), 400)

    try:
        if users.create_user(username, email, password, display_name) is not None:
            return (jsonify(), 200)
        else:
            return (
                jsonify({"error": "cannot create user with that information"}),
                400,
            )
    except (Exception, DatabaseError) as err:
        return (jsonify({"error": err}), 500)


@auth.route("/me")
@jwt_required()
def me():
    return (
        jsonify(
            current_user.to_dict(False)
        ),
        200,
    )


@auth.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    return (jsonify({"error": "TODO"}), 501)
