#!/usr/bin/env python3
"""
flask app to render webpages....
"""

from flask import Flask, render_template, send_file, jsonify
from jinja2 import TemplateNotFound
import platform


webapp = Flask(__name__)
webapp.config['TEMPLATES_AUTO_RELOAD'] = True
webapp.config['SECRET_KEY'] = "mypennypilotapp"


@webapp.route("/", methods=["GET"])
def index():
    """returns the index page"""
    try:
        return render_template(f"index_{platform.system()}.html")
    except TemplateNotFound:
        return f"create a symlink for {platform.system()}"

@webapp.route("/favicon.ico", methods=["GET"])
def favicon():
    """returns the favicon"""
    return send_file("favicon_light.ico")

@webapp.errorhandler(404)
def notFoundhandler():
    """returns the error 404 page"""
    return jsonify(error="Page not Found")

@webapp.errorhandler(403)
def forbiddenHandler():
    """returns user forbidden page"""
    return jsonify(error="This page is forbidden")


@webapp.errorhandler(401)
def authorizeYourself():
    """returns the user to authorization page"""
    return jsonify(error="Please Sign in to view this page")

if __name__ == "__main__":
    webapp.run(port="5050", debug=True, host="0.0.0.0")
