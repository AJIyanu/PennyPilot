#!/usr/bin/python
"""base model for sales[goods and services] in the app
"""

from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict
from objects.models.basemodel import BaseModel, Base


class Sales(BaseModel, Base):
    """This is the class for Sales
    """

    __tablename__ = "sales"
    user_id = Column(String(60), ForeignKey("user.id"), nullable=False)
    stock_id = Column(String(60), ForeignKey('stock.id'), nullable=False)
    name = Column(String(30), nullable=False)
    cost_price = Column(Float(precision=2))
    selling_price = Column(Float(precision=2))
    quantity = Column(Integer())
    customer_id = Column(String(60), ForeignKey('customer.id'))


    def __init__(self, *args, **kwargs):
        """
        initializes the class
        """
        super().__init__(args, kwargs)
        self.stock_id = kwargs.get("stock_id")
        self.user_id = kwargs.get("user_id")
        self.name = kwargs.get("name")
        if "customer_id" in kwargs:
            self.customer_id = kwargs.get("customer_id")
        self.cost_price = int(kwargs.get("cost", 0))
        self.selling_price = int(kwargs.get("sell", 0))
        self.quantity = int(kwargs.get("qty", 1))
