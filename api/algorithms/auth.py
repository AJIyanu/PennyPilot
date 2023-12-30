#!/usr/bin/env python3
"""does authorization and registration
"""


from objects.models.users import User


def authorizer_user(email: str, pwd: str) -> str:
    """autorizes user and returns json object"""
    return User.userObj(email=email, pwd=pwd)

def registerUser(**kwargs):
    """registers user to databse"""
    validate = ["email", "firstname", "surname", "password"]
    for check in validate:
        if check not in kwargs:
            return None
    user = User(**kwargs)
    try:
        user.save()
    except Exception:
        return None
    return user.id
