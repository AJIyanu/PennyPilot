#!/usr/bin/python
"""base model for products[goods and services] in the app
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict
from users import Base

class Stock(Base):
    """This is the class for Stock
    """

    __tablename__ = "stock"
    id = Column(String(60), nullable=False, unique=True, primary_key=True)
    product_id = Column(String(60), ForeignKey('product.id'), nullable=False)
    product = relationship('Product', foreign_keys=['products_id'], back_populates='stock')
    name = Column(String(30), nullable=False)
    cost_price = Column(Float(precision=2))
    selling_price = Column(Float(precision=2))
    stock_qty = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
