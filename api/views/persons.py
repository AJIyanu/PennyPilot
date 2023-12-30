#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort, request
from views import app_views
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_jwt_extended import get_jwt, create_refresh_token
import base64

from ..algorithms.auth import authorizer_user, registerUser



@app_views.route("/signin", methods=['GET'])
def signin():
    """signs in user and return token"""
    details = request.headers
    if "authorization" not in details:
        abort(404)
    details: str = details.get("authorization")
    if not details.startswith('Basic'):
        abort(404)
    details = details.split(" ").pop()
    details = base64.b64decode(details).decode("utf-8")
    details = details.split(":", 1)
    user = authorizer_user(details[0], details[1])
    if user is None:
        abort(404)
    payload = {
        "surname": user.surname,
        "firstname": user.firstname
        }
    access_token = create_access_token(identity=user.id, additional_claims=payload)
    return jsonify({ "status": "successful login", "x-token": access_token })

@app_views.route("/signup", methods=["POST"])
def signup():
    """sign up users"""
    details = request.json
    user_id = registerUser(**details)
    if user_id is None:
        return jsonify(error="User not registered"), 400
    return jsonify({ "status": "User Registered Successfully", "userId": user_id }), 200
