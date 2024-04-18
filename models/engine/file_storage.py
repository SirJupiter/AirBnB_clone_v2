#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    the_classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        all_the_objects = {}

        if cls:
            for key, value in self.__objects.items():
                class_name, class_id = key.split('.')
                if cls.__name__ == class_name:
                    all_the_objects[key] = value
            return all_the_objects

        for value in self.__objects.values():
            if hasattr(value, '_sa_instance_state'):
                delattr(value, '_sa_instance_state')

        return self.__objects

    # def get_all(self, key=None):
    #     """Gets all objects from the storage
    #      optionally filtered by the key"""
    #     print(self.all())
    #     if not key:
    #         return [str(i) for i in self.all().values()]
    #     return list(filter(
    #         lambda lookup_success: key in str(lookup_success),
    #         self.all().values()
    #     ))

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file

        For converting the python objects into python dictionary,
        so they can be stred into file storage:
        This is the serialization process
        """
        # with open(FileStorage.__file_path, 'w') as f:
        #     temp = {}
        #     temp.update(FileStorage.__objects)
        #     for key, val in temp.items():
        #         temp[key] = val.to_dict()
        #     json.dump(temp, f)

        temp = {}

        for key, value in self.__objects.items():
            temp[key] = value.to_dict()

        with open(self.__file_path, 'w') as file:
            json.dump(temp, file)

    def reload(self):
        """Loads storage dictionary from file"""

        # try:
        #     temp = {}
        #     with open(FileStorage.__file_path, 'r') as f:
        #         temp = json.load(f)
        #         for key, val in temp.items():
        #             self.all()[key] = classes[val['__class__']](**val)
        # except FileNotFoundError:
        #     pass

        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r') as info:
                try:
                    file_content = json.load(info)

                    for key, val in file_content.items():
                        c_name, c_key = key.split('.')

                        boss_class = self.the_classes[c_name]
                        res = boss_class(**val)
                        self.__objects[key] = res
                except Exception:
                    print('Unable to serialize')
                    exit(0)

    def delete(self, obj=None):
        """delete existing element"""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            del self.__objects[key]
            # was self.all() before

    def close(self):
        """calls reload()"""
        self.reload()
