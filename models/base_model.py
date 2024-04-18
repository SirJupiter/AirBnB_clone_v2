#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime, timezone
# from models import storage_type
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def get_utc_now():
    """Function gets the instant time"""
    return datetime.now(timezone.utc)


class BaseModel:
    """A base class for all hbnb models"""

    # create SQLAlchemy representations for id, created_at & updated_at
    # variables to be slotted into class for creating the tables

    time_format = '%Y-%m-%dT%H:%M:%S.%f'
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, default=get_utc_now, nullable=False)
    updated_at = Column(DateTime, default=get_utc_now, nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""

        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            # storage.new(self)

        else:
            dates = ["created_at", "updated_at"]

            for key, value in kwargs.items():
                if key in dates:
                    value = datetime.fromisoformat(value)
                if key != '__class__':
                    setattr(self, key, value)

            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.now()
            if 'updated_at' not in kwargs:
                self.updated_at = datetime.now()
            # kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
            #                                          '%Y-%m-%dT%H:%M:%S.%f')
            # kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
            #                                          '%Y-%m-%dT%H:%M:%S.%f')
            # del kwargs['__class__']
            # self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    # @classmethod
    # def all(cls):
    #     """"""
    #     return storage.get_all(cls.__name__)

    # @classmethod
    # def count(cls):
    #     """"""
    #     return len(cls.all())

    # @classmethod
    # def show(cls, ids):
    #     """"""
    #     return storage.get(f"{cls.__name__}.{ids}")

    # @classmethod
    # def destroy(cls, ids):
    #     """"""
    #     storage.delete(f"{cls.__name__}.{ids}")

    # @classmethod
    # def update(cls, ids, attr=None, value=None):
    #     """"""
    #     obj = cls.show()
    #     if isinstance(attr, dict):
    #         for key, value in attr.items():
    #             setattr(obj, key, value)
    #     else:
    #         setattr(obj, attr, value)
    #     obj.save()

    def delete(self):
        """delete object"""
        from models import storage
        storage.delete(self)

    def to_dict(self):
        """Convert instance into dict format"""

        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__

        for k in dictionary:
            if type(dictionary[k]) is datetime:
                dictionary[k] = dictionary[k].isoformat()
        if '_sa_instance_state' in dictionary.keys():
            del dictionary['_sa_instance_state']
        return dictionary
