#!/usr/bin/python
"""base model for people in the app
"""

from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
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
    storeName = Column(String(60))
    isActive = Column(Boolean, default=False)
    email: str = Column(String(60), nullable=False, unique=True )
    __hash_password: str = Column(String(128), nullable=False)


    def __init__(self, *args, **kwargs):
        """
        initializes the class
        """
        super().__init__(args, kwargs)
        if "password" in kwargs.keys():
            self.__hash_password = hashpwd(kwargs['password'])
        self.firstname = kwargs.get("firstname")
        self.surname = kwargs.get("surname")
        self.email = kwargs.get("email")

    def __validate_user(self, password: str) -> bool:
        """returns true if there is a match"""
        return pwdmatch(self.__hash_password, password)

    @classmethod
    def userObj(self, email: str, pwd: str):
        """returns self if validated"""
        from objects import storage
        user = storage.getuser(self, { "email": email })
        if len(user) < 1:
            return None
        obj = user[0]
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
