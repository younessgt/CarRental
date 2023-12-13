#!/usr/bin/python3
""" Containing User class """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from flask_login import UserMixin
from sqlalchemy.orm import relationship


class User(BaseModel, Base, UserMixin):
    """ Representing the User class """

    __tablename__ = 'users'
    username = Column(String(80), nullable=False, unique=True)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    user_cars = relationship("Car", backref="user",
                             cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes User"""
        super().__init__(*args, **kwargs)
