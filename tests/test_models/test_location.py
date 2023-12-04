#!/usr/bin/python3
""" Testing Location Class """

from models.location import Location
from datetime import datetime
from models.base_model import BaseModel
import models
import unittest
from unittest import mock


class TestLocation(unittest.TestCase):
    """ testing cases for Location class """

    def test_attribute(self):
        """ testing the attributes """
        location1 = Location()
        self.assertTrue(hasattr(location1, "name"))
        self.assertTrue(hasattr(location1, "id"))
        self.assertTrue(hasattr(location1, "created_at"))
        self.assertTrue(hasattr(location1, "updated_at"))
        self.assertIsInstance(location1.id, str)
        self.assertIsInstance(location1.created_at, datetime)
        self.assertIsInstance(location1.updated_at, datetime)
        self.assertEqual(location1.name, None)

    def test_instant(self):
        """testing instantiation"""

        location2 = Location()
        self.assertIsInstance(location2, Location)
        self.assertTrue(issubclass(Location, BaseModel))

    def test_to_dict(self):
        """ testing to_dict method """
        location3 = Location()
        location3.name = "Rabat"
        cr = location3.created_at
        up = location3.updated_at

        location_dict = location3.to_dict()
        self.assertEqual(type(location_dict), dict)
        self.assertIn("__class__", location_dict)
        self.assertEqual(location_dict['__class__'], 'Location')
        self.assertEqual(cr.isoformat(), location3.to_dict()["created_at"])
        self.assertEqual(up.isoformat(), location3.to_dict()["updated_at"])
        self.assertEqual(location_dict["name"], "Rabat")

        self.assertFalse("_sa_instance_state" in location_dict)

    @mock.patch('models.storage')
    def test_save(self, mock_storage):
        """ testing save method """
        location4 = Location()
        old_cr = location4.created_at
        old_up = location4.updated_at

        location4.save()

        new_cr = location4.created_at
        new_up = location4.updated_at

        self.assertNotEqual(old_up, new_up)
        self.assertEqual(old_cr, new_cr)
        self.assertTrue(mock_storage.new.called)
        self.assertTrue(mock_storage.save.called)
