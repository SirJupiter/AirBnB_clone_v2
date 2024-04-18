#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
# from models.engine.file_storage import FileStorage
from models.engine import file_storage
# from models.engine.db_storage import DBStorage
from models.engine import db_storage
from os import getenv

storage_type = getenv('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    storage = db_storage.DBStorage()
else:
    storage = file_storage.FileStorage()

storage.reload()
