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
            print("incomplete parameters")
            return None
    user = User(**kwargs)
    print(user.to_dict())
    try:
        user.save()
    except Exception as msg:
        return None
    return user.id
