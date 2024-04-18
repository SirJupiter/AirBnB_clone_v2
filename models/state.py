#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models import storage_type

from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class.
     Will become a table inside database
       """

    __tablename__ = 'states'

    if storage_type == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship(
            "City", cascade='all, delete, delete-orphan', backref='state')
    else:
        name = ""

    @property
    def c_cities(self):
        """retuns list of City instances where
        state_id == current State.id
        """
        from models import storage
        linked_cities = []
        c_cities = storage.all(City)

        for c_c in c_cities.values():
            if c_c.state_id == self.id:
                linked_cities.append(c_c)
        return linked_cities
