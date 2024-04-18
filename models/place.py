#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models import storage
from models import storage_type
# from models.city import City
# from models.user import User
from sqlalchemy.sql.schema import Table
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from models.amenity import Amenity
# from models.review import Review


p = Column('place_id', String(60), ForeignKey('places.id'), primary_key=True,
           nullable=False)
a = Column('amenity_id', String(60), ForeignKey('amenities.id'),
           primary_key=True, nullable=False)

if storage_type == 'db':
    place_amenity = Table('place_amenity', Base.metadata, p, a)


class Place(BaseModel, Base):
    """ A place to stay
     Will become a table in database
    """
    __tablename__ = "places"

    if storage_type == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_is = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenities = relationship(
            'Amenity', secondary=place_amenity, viewonly=False,
            backref='place_amenities')
        reviews = relationship(
            'Review', cascade='all, delete, delete-orphan', backref='place')
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    @property
    def amenitiess(self):
        """returns list of Amenity instances
        based on the attribute amenity_ids that contains
        all Amenity.id linked to Place
        """
        all_amenities = storage.all(Amenity)

        amenity_list = []
        for item in all_amenities.values():
            if item.id in self.amenity_ids:
                amenity_list.append(item)
        return amenity_list

    @amenitiess.setter
    def amenitiess(self, obj):
        """adds an Amenity.id to the attribute amenity_ids
        and accepts only amenity objects
        """
        if obj:
            if isinstance(obj, Amenity):
                if obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)
