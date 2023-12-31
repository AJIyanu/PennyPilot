#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from typing import Dict

# models import
from objects.models.users import User, Base
from objects.models.customers import Customer
from objects.models.sales import Sales
from objects.models.products import Product
from objects.models.stock import Stock

classes = {
    "User": User,
    "Customer": Customer,
    "Sales": Sales,
    "Stock": Stock,
    "Product": Product
    }


class MySqlVault:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None
    clses = classes

    def __init__(self):
        """Instantiate a DBStorage object"""
        self.__engine = create_engine('mysql+pymysql://admin:pwd@localhost/pennypilot')

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls is None:
            return None

        if cls not in classes.values():
            cls = classes.get(cls)
            if cls is None:
                return None

        user = self.__session.query(cls).filter_by(id=id)
        return user.first()

    def getuser(self, cls, filter: Dict):
        """return objects based on filter query"""
        if cls is None:
            return  None

        if cls in classes:
            obj = classes[cls]
        elif cls in classes.values():
            obj = cls
        folk = self.__session.query(obj).filter_by(**filter)
        return [data for data in folk]

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(self.all(clas).values())
        else:
            count = len(self.all(cls).values())

        return count
