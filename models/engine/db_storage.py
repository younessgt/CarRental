#!/usr/bin/python3
""" Contain the Dbstorage class """

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import BaseModel, Base
from models.location import Location
from models.car import Car

list_class = {"Location": Location, "Car": Car}


class Dbstorage:
    """ class to interact with MySql Database """

    __engine = None
    __session = None

    def __init__(self):
        """ constructor module
        initializing a Dbstorage object"""

        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def new(self, obj):
        """ Adding  the object to the session"""
        self.__session.add(obj)

    def add(self, objs):
        """ Adding a list of objects to the session"""
        for obj in objs:
            self.__session.add(obj)

    def save(self):
        """ commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from the current database session obj if not None """
        if obj is not None:
            self.__session.delete(obj)

    def all(self, cls=None):
        """Retrieving data for each class from a database."""

        new_dict = {}
        for clas in list_class:
            """ the final check for if is for checking
            for example if cls='Location' """
            if cls is None or cls is list_class[clas] or cls is clas:
                list_obj = self.__session.query(list_class[clas]).all()
                for obj in list_obj:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def get(self, cls, id):
        """ get method based on the class name and its id """

        if cls not in list_class.values():
            return None
        list_obj = self.__session.query(cls).all()
        for obj in list_obj:
            if obj.id == id:
                return obj
        return None

    def update_status(self, car_id, new_status):
        """ updating the object status """
        from models import storage
        car = storage.get(Car, car_id)
        if car:
            car.status = new_status
            car.update()
            return True
        return False

    def close(self):
        """ calling remove method to close and remove the session"""
        self.__session.remove()