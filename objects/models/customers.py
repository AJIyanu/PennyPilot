#!/usr/bin/python
"""base model for products[goods and services] in the app
"""

import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict
from objects.models.users import User, Base

class Customer(Base):
    """This is the class for Product
    """

    __tablename__ = "customer"
    id = Column(String(60), nullable=False, unique=True, primary_key=True)
    user_id = Column(String(30), ForeignKey("user.id"))
    firstname = Column(String(30), nullable=False)
    surtname = Column(String(30))
    phone = Column(String(20))
    address = Column(String(128))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
