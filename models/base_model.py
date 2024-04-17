#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """A base class for all hbnb models"""
    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        dates = ["created_at", "updated_at"]
        checks = []
        for i in kwargs.keys():
            if i not in dates:
                checks.append(True)
        if not kwargs or checks:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
            if kwargs:
                self.__dict__.update(kwargs)
        else:
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            del kwargs['__class__']
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
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
        storage.delete(self)

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary
