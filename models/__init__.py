#!/usr/bin/python3
""" initialize the models package
the storage attribute will be loaded from this file"""

from models.engine.db_storage import Dbstorage

storage = Dbstorage()
storage.reload()
