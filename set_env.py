#!/usr/bin/python3
"""Sets environment variables"""

from os import environ

environ['HBNB_ENV'] = 'dev'
environ['HBNB_MYSQL_USER'] = 'hbnb_dev'
environ['HBNB_MYSQL_PWD'] = 'hbnb_dev_pwd'
environ['HBNB_MYSQL_HOST'] = 'localhost'
environ['HBNB_MYSQL_DB'] = 'hbnb_dev_db'
environ['HBNB_TYPE_STORAGE'] = 'db'
