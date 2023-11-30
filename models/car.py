#!/usr/bin/python3
""" Containing Car class """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey


class Car(BaseModel, Base):
    """ Representing the Car class """

    __tablename__ = 'cars'
    name = Column(String(128), nullable=False)
    fuel = Column(String(128), nullable=False)
    rent_price = Column(Integer, nullable=False, default=0)
    status = Column(String(128), nullable=False)
    """location_id = Column(String(60), ForeignKey('locations.id'),
                         nullable=False)"""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)
