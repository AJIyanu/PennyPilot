#!/usr/bin/python
"""base model for people in the app
"""

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from typing import Self
from argon2 import PasswordHasher, exceptions

pwdhsh = PasswordHasher()

from objects.models.basemodel import Base, BaseModel

class User(BaseModel, Base):
    """
    This class describes the basic attribute of every
    human users
    """

    __tablename__ = "user"
    firstname: str = Column(String(30), nullable=False)
    surname: str = Column(String(30), nullable=False)
    email: str = Column(String(60), nullable=False)
    __hash_password: str = Column(String(128), nullable=False)


    def __init__(self, *args, **kwargs):
        """
        initializes the class
        """
        super().__init__(args, kwargs)
        if "password" in kwargs.keys():
            self.__hash_password = hashpwd(kwargs['password'])

    def __validate_user(self, password: str) -> bool:
        """returns true if there is a match"""
        return pwdmatch(self.__hash_password, password)

    @classmethod
    def userObj(self, email: str, pwd: str) -> Self:
        """returns self if validated"""
        from objects import storage
        user = storage.getuser(self, email=email)
        if user == None:
            return None
        obj: Self = user[0]
        if obj.__validate_user(pwd):
            return obj
        return None

    def resetpwd(self, pwd:str) -> None:
        """resets password"""
        self.__hash_password = hashpwd(pwd)
        self.save()



def hashpwd(password: str):
    """returns hashed passowrd"""
    if password.startswith('argon2id$v=19$'):
        return password
    return pwdhsh.hash(password)

def pwdmatch(savedpwd: str, pwd: str):
    """returns true if match otherwise false"""
    try:
        return pwdhsh.verify(savedpwd, pwd)
    except exceptions.VerifyMismatchError:
        return False
