#!/usr/bin/python
"""base model for people in the app
"""

import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict

Base = declarative_base()


class User(Base):
    """
    This class describes the basic attribute of every
    human users
    """

    __tablename__ = "user"
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    firstname = Column(String(30), nullable=False)
    surname = Column(String(30), nullable=False)
    email= Column(String(60), nullable=False)
    hash_password = Column(String(128), nullable=False)


    def __init__(self, *args, **kwargs):
        """
        initializes the class
        """
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            try:
                self.id = args[0]
                self.surname = args[1]
                self.firstname = args[2]
            except Exception:
                pass
        else:
            if "id" not in kwargs.keys():
                self.id = str(uuid.uuid4())
            try:
                kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
                kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            except KeyError:
                self.created_at = datetime.now()
                self.updated_at = datetime.now()
            finally:
                self.__dict__.update(kwargs)
        from models import storage
        storage.new(self)

    def __str__(self):
        """Returns a string representation of the instance"""
        return '[{}] ({}) {}'.format(self.__class__.__name__, self.id, self.__dict__)

    def to_dict(self):
        """converts to dictionary"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if "_sa_instance_state" in dictionary:
            del dictionary["_sa_instance_state"]
        return dictionary

    def save(self):
        """save to database"""
        self.updated_at = datetime.now()
        from models import storage
        storage.save()

    def show_all(self):
        """show all intances"""
        from models import storage
        storage.reload()
        patients = storage.all(self)
        return patients

    @classmethod
    def user_by_id(self, id:str = None) -> Dict:
        """returns user instance by id"""
        from models import storage
        try:
            me = storage.user_by_id(self, id)
        except NoResultFound:
            return None
        return me

    @classmethod
    def update_me(self, id: str, **kwargs) -> None:
        """update class"""
        from models import storage
        try:
            me = storage.cls_by_id(self, id)
        except NoResultFound:
            return None
        me_lst = dir(me)
        for key in kwargs:
            if key[:2] != "__" and key in me_lst:
                setattr(me, key, kwargs[key])
        me.save()
        return

    def purge(self):
        """deletes object"""
        from models import storage
        storage.delete(self)
