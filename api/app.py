#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from views import app_views
from flask import Flask, jsonify
from flask_cors import (CORS, cross_origin)
from flask_jwt_extended import JWTManager
from datetime import timedelta

import os

from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'roseismysecretkey'
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=2)
app.config['JWT_SECRET_KEY'] = 'roseismysecretekey'
CORS(app, resources={r"/api/*": {"origins": "*"}})
jwt = JWTManager(app)


@app.before_request
def handle_before():
    """handles stuff before request is made"""
    pass


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def close_db(error):
     """ Close Storage """
     storage.close()

@app.errorhandler(401)
def not_authorized(error) -> str:
    """handling unauthorized shits"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """authorized but not aloowed"""
    return jsonify({"error": "Forbidden"}), 403



if __name__ == "__main__":
    with app.test_request_context():
        print(app.url_map)
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
