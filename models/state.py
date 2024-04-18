#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
# from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class.
     Will become a table inside database
       """

    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship(
        "City", cascade='all, delete, delete-orphan', backref='state')
    # name = ""
