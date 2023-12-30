#!/usr/bin/python
"""base model for products[goods and services] in the app
"""

from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict
from objects.models.basemodel import BaseModel, Base


class Product(BaseModel, Base):
    """This is the class for Product
    """

    __tablename__ = "product"
    user_id = Column(String(30), ForeignKey("user.id"), nullable=False)
    name = Column(String(30), nullable=False, unique=True)
    cost_price = Column(Float(precision=2))
    selling_price = Column(Float(precision=2))
    pack = Column(Integer())
    carton = Column(Integer())


    def __init__(self, *args, **kwargs):
        """
        initializes the class
        """
        super().__init__(args, kwargs)
