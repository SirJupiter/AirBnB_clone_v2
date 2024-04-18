#!/usr/bin/python3
"""Sets environment variables"""

from os import environ

environ['HBNB_ENV'] = 'dev'
environ['HBNB_MYSQL_USER'] = 'your_mysql_username'
environ['HBNB_MYSQL_PWD'] = 'your_mysql_password'
environ['HBNB_MYSQL_HOST'] = 'your_mysql_host'
environ['HBNB_MYSQL_DB'] = 'your_mysql_database'
environ['HBNB_TYPE_STORAGE'] = 'db'
