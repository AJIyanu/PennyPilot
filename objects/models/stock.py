#!/usr/bin/python
"""base model for products[goods and services] in the app
"""

from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict
from objects.models.basemodel import BaseModel, Base


class Stock(BaseModel, Base):
    """This is the class for Stock
    """

    __tablename__ = "stock"
    user_id = Column(String(60), ForeignKey("user.id"), nullable=False)
    product_id = Column(String(60), ForeignKey('product.id'), nullable=False)
    product = relationship('Product', foreign_keys=['products_id'], back_populates='stock')
    name = Column(String(30), nullable=False)
    cost_price = Column(Float(precision=2))
    selling_price = Column(Float(precision=2))
    stock_qty = Column(Integer, nullable=False)




    def __init__(self, *args, **kwargs):
        """
        initializes the class
        """
        super().__init__(args, kwargs)
