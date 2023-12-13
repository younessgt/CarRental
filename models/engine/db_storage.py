#!/usr/bin/python3
""" Contain the Dbstorage class """

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import BaseModel, Base
from models.location import Location
from models.car import Car
from models.user import User

list_class = {"Location": Location, "Car": Car, "User": User}


class Dbstorage:
    """ class to interact with MySql Database """

    __engine = None
    __session = None

    def __init__(self):
        """ constructor module
        initializing a Dbstorage object"""

        MYSQL_USER = getenv('MYSQL_USER')
        MYSQL_PWD = getenv('MYSQL_PWD')
        MYSQL_HOST = getenv('MYSQL_HOST')
        MYSQL_DB = getenv('MYSQL_DB')
        ENV = getenv('ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(MYSQL_USER,
                                             MYSQL_PWD,
                                             MYSQL_HOST,
                                             MYSQL_DB))
        if ENV == "test":
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
        """for efficienty we shoud replace all() by
        obj = self.__session.query(cls).filter_by(id=id).first()
        return obj"""
        list_obj = self.__session.query(cls).all()
        for obj in list_obj:
            if obj.id == id:
                return obj
        return None

    def get_by_username(self, cls, username):
        """ method to retrieve a user object based on the username """

        if cls not in list_class.values():
            return None

        obj = self.__session.query(cls).filter_by(username=username).first()
        return obj

    def get_by_email(self, cls, email):
        """ method to retrieve a user object based on the email """

        if cls not in list_class.values():
            return None

        obj = self.__session.query(cls).filter_by(email=email).first()
        return obj

    def update_status(self, car_id, new_status, userid):
        """ updating the object status (this method is for the car object)"""
        from models import storage
        car = storage.get(Car, car_id)
        if car:
            car.status = new_status
            if new_status == "Booked":
                car.user_id = userid
            else:
                car.user_id = None
            car.update()
            return True
        return False

    def close(self):
        """ calling remove method to close and remove the session"""
        self.__session.remove()
