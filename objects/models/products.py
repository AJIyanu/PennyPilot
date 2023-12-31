#!/usr/bin/python
"""base model for products[goods and services] in the app
"""

from sqlalchemy import Column, String, Float, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
import math
from objects.models.basemodel import BaseModel, Base


class Product(BaseModel, Base):
    """This is the class for Product
    """

    __tablename__ = "product"
    user_id = Column(String(60), ForeignKey("user.id"), nullable=False)
    name = Column(String(30), nullable=False, unique=True)
    cost_price = Column(Float(precision=2))
    selling_price = Column(Float(precision=2))
    pack = Column(Integer())
    carton = Column(Integer())
    isActive = Column(Boolean, default=True)


    def __init__(self, *args, **kwargs):
        """
        initializes the class
        """
        super().__init__(args, kwargs)
        self.name = kwargs.get("name")
        self.user_id = kwargs.get("user_id")
        self.cost_price = float(kwargs.get("cost"))
        self.selling_price = float(kwargs.get("sell"))
        self.pack = int(kwargs.get("pack"))
        self.carton = int(kwargs.get("carton"))

    def sellPriceByPercentProfit(self, profit):
        """sets selling price by percent profit rounds up
            to nearest naira
        """
        cost = self.cost_price
        sell = int(profit) * cost / 100
        sell += cost
        roundedNum = round(math.ceil(sell), -1)
        if sell > roundedNum:
            roundedNum += 10
        self.selling_price = roundedNum
        self.save()

    def toggleProductActive(self):
        """removes product and restore"""
        if self.isActive == False:
            self.isActive = True
            self.save()
            return
        self.isActive = False
        self.save()
