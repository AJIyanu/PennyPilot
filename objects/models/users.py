#!/usr/bin/python
"""base model for people in the app
"""

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict

from objects.models.basemodel import Base, BaseModel

class User(BaseModel, Base):
    """
    This class describes the basic attribute of every
    human users
    """

    __tablename__ = "user"
    firstname = Column(String(30), nullable=False)
    surname = Column(String(30), nullable=False)
    email= Column(String(60), nullable=False)
    hash_password = Column(String(128), nullable=False)


    def __init__(self, *args, **kwargs):
        """
        initializes the class
        """
        super().__init__(args, kwargs)
