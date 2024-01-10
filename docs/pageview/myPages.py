#!/usr/bin/python3
"""my pages display"""


from flask import render_template, url_for, request, redirect
from flask_login import login_required, UserMixin, login_user, logout_user, current_user
from redis import Redis
import requests
import base64
import uuid
import json

# from docs.pageview.myPages import webapp
# from docs.webpage import userLogin
from . import app_page



users = Redis(decode_responses=True)

class Trader(UserMixin):
    """performs user registration"""

    userDict = {}
    userId = None
    userToken = None
    fresh = False


    def __init__(self, **kwargs) -> None:
        """Returns True is user credential is okay and false otherwise"""
        authstring = f"{kwargs.get('email')}:{kwargs.get('pwd')}"
        authstring = base64.b64encode(authstring.encode('utf-8')).decode('utf-8')
        authstring = f"Basic {authstring}"
        if "userId" in kwargs:
            for keys, value in kwargs.items():
                setattr(self, keys, value)
            return
        user = requests.get("http://127.0.0.1:5000/api/signin", headers={"Authorization": authstring})
        if user.status_code != 200:
            return
        self.userDict = user.json().get("user_data")
        self.userId = self.__userDict.get("id")
        self.userToken = user.json().get("x-token")
        self.fresh = True

    def is_authenticated(self):
        """returns True and None. Overload method"""
        if self.userId != None:
            return True
        return False

    def is_active(self):
        """checks if user actively logged in"""
        if self.userToken != None:
            if self.userDict.get("isAtctive") == True:
                return True
            return False
        return False

    def get_id(self):
        return self.userId

    @classmethod
    def deserialize(cls, userstr):
        """returns user class"""
        user = json.loads(userstr)
        return cls(**user)

def addUser(email, password):
    """creates User Object and adds to user"""
    newUser = Trader(email=email, pwd=password)
    if newUser.get_id() is None:
        return
    altId = str(uuid.uuid4())
    users.set(altId, json.dumps(newUser.__dict__))
    return newUser


@app_page.route("/signin", methods=["POST"])
def signinUser():
    """logs in user"""
    userID = addUser(**request.form)
    if userID == None:
        return redirect(url_for("index"))
    login_user(userID)
    return redirect("/dashboard")

@app_page.route("/dashboard", methods=["GET"])
@login_required
def userDashboard():
    """return dashboard page"""
    user = current_user
    payload = {
        "firstname": user.userDict.get("firstname"),
        "surname": user.userDict.get("surname"),
        "storname": user.userDict.get("storeName")
        }
    xToken = user.userToken
    print(xToken, payload)
    return render_template("dashboard.html")

@app_page.route('/dashboard/<subpage>', methods=["GET"])
@login_required
def iFramepageload(subpage):
    """returns the subwebpages"""
    return render_template(f"{subpage}.html")
