#!/usr/bin/python
"""base model for products[goods and services] in the app
"""

import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Float, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict
from users import Base

class Product(Base):
    """This is the class for Product
    """

    __tablename__ = "product"
    id = Column(String(60), nullable=False, unique=True, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)
    stock = relationship("Stock", back_populates='product')
    cost_price = Column(Float(precision=2))
    selling_price = Column(Float(precision=2))
    pack = Column(Integer())
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    carton = Column(Integer())
