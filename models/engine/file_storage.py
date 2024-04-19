#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    the_classes = {
            'BaseModel': BaseModel,
            'User': User,
            'Place': Place,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Review': Review
        }

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        all_objects = {}

        if cls:
            for key, value in self.__objects.items():
                cls_name, cls_id = key.split('.')
                if cls.__name__ == cls_name:
                    all_objects[key] = value
                if hasattr(value, '_sa_instance_state'):
                    delattr(value, '_sa_instance_state')
            return all_objects

        for value in self.__objects.values():
            if hasattr(value, '_sa_instance_state'):
                delattr(value, '_sa_instance_state')

        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        if hasattr(obj, '_sa_instance_state'):
            delattr(obj, '_sa_instance_state')

        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(self.__file_path, 'w') as file:
            temp_dict = {}
            temp_dict.update(self.__objects)
            for key, val in temp_dict.items():
                temp_dict[key] = val.to_dict()
            json.dump(temp_dict, file)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(self.__file_path, 'r') as file:
                temp = json.load(file)
                for key, val in temp.items():
                    self.all()[key] = self.the_classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        ''' deletes the object obj from the attribute
            __objects if it's inside it
        '''
        if obj is None:
            return

        obj_key = obj.to_dict()['__class__'] + '.' + obj.id

        if obj_key in self.__objects.keys():
            del self.__objects[obj_key]

    def close(self):
        """Call the reload method"""
        self.reload()
