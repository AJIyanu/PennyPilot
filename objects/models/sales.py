#!/usr/bin/python
"""base model for sales[goods and services] in the app
"""

import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict
from users import Base

class Sales(Base):
    """This is the class for Sales
    """

    __tablename__ = "sales"
    id = Column(String(60), nullable=False, unique=True, primary_key=True)
    user_id = Column(String(60), ForeignKey("user.id"), nullable=False)
    stock_id = Column(String(60), ForeignKey('stock.id'), nullable=False)
    stock = relationship("Stock", back_populates='stock')
    name = Column(String(30), nullable=False)
    cost_price = Column(Float(precision=2))
    selling_price = Column(Float(precision=2))
    quantity = Column(Integer())
    customer_id = Column(String(60) ForeignKey('customer.id'))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
