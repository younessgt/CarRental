#!/usr/bin/python3
""" Containing Location Class """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship

"""many to many relationship """

car_location = Table('car_location', Base.metadata,
                     Column('car_id', String(60),
                            ForeignKey('cars.id', onupdate='CASCADE',
                                       ondelete='CASCADE'),
                            primary_key=True),
                     Column('location_id', String(60),
                            ForeignKey('locations.id', onupdate='CASCADE',
                                       ondelete='CASCADE'),
                            primary_key=True))


class Location(BaseModel, Base):
    """ Representing the Location class """

    __tablename__ = 'locations'
    name = Column(String(128), nullable=False)
    cars = relationship("Car", secondary=car_location,
                        backref="location", viewonly=False)

    def __init__(self, *args, **kwargs):
        """initializes location"""
        super().__init__(*args, **kwargs)
