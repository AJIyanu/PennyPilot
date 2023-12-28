#!/usr/bin/python
"""base model for products[goods and services] in the app
"""

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict
from objects.models.basemodel import BaseModel, Base

class Customer(BaseModel, Base):
    """This is the class for Product
    """

    __tablename__ = "customer"
    user_id = Column(String(30), ForeignKey("user.id"))
    firstname = Column(String(30), nullable=False)
    surname = Column(String(30))
    phone = Column(String(20))
    address = Column(String(128))

    def __init__(self, *args, **kwargs):
        """
        initializes the class
        """
        super().__init__(args, kwargs)
