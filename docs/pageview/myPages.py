#!/usr/bin/python3
"""my pages display"""


from flask import render_template, url_for
from flask_login import login_required, LoginManager, UserMixin, login_user, logout_user
import requests
import base64
import uuid

from docs.pageview.myPages import webapp
from . import app_page


userLogin = LoginManager()
userLogin.init_app(webapp)

users = {}

class Trader(UserMixin):
    """performs user registration"""

    __userDict = {}
    __userId = None
    __userToken = None


    def __init__(self, email: str, pwd: str) -> None:
        """Returns True is user credential is okay and false otherwise"""
        if email is None or pwd is None:
            return
        authstring = f"{email}:{pwd}"
        authstring = base64.b64encode(authstring.encode('utf-8')).decode('utf-8')
        authstring = f"Basic {authstring}"
        user = requests.get("http://127.0.0.1:5000/api/signin", headers={"Authorization": authstring})
        if user.status_code != "200":
            return
        self.__userDict = user.json().get("user_data")
        self.__userId = self.__userDict.get("id")
        self.__userToken = user.json().get("x-token")

    def is_authenticated(self):
        """returns True and None. Overload method"""
        if self.__userId != None:
            return True
        return False

    def is_active(self):
        """checks if user actively logged in"""
        if self.__userToken != None:
            if self.__userDict.get("isAtctive") == True:
                return True
            return False
        return False

    def get_id(self):
        return self.__userId

def addUser(email, pwd):
    """creates User Object and adds to user"""
    newUser = Trader(email=email, pwd=pwd)
    if newUser.get_id() is None:
        return
    altId = uuid.uuid4()
    users.update({altId: newUser})
    return altId

@userLogin.user_loader
def load_user(user_id):
    return users.get(user_id)


@app_page.route("/signin", methods=["POST"])
def signinUser():
    """logs in user"""
    userID = addUser(**requests.form)
    if userID == None:
        return url_for("index")
    login_user(users.get(userID))
    return url_for("userDashboard")

@app_page.route("/dashboard", methods=["GET"])
@login_required()
def userDashboard():
    """return dashboard page"""
    return render_template("dasboard.html")
