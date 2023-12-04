#!/usr/bin/python3
""" Testing Car Class """

from models.car import Car
from datetime import datetime
from models.base_model import BaseModel
import models
import unittest
from unittest import mock


class TestCar(unittest.TestCase):
    """ testing cases for Car class """

    def test_attribute(self):
        """ testing the attributes """
        car1 = Car(name="CC", fuel="Gaso", rent_price=75, status="unbooked")
        self.assertTrue(hasattr(car1, "name"))
        self.assertTrue(hasattr(car1, "rent_price"))
        self.assertTrue(hasattr(car1, "status"))
        self.assertTrue(hasattr(car1, "fuel"))
        self.assertTrue(hasattr(car1, "id"))
        self.assertTrue(hasattr(car1, "created_at"))
        self.assertTrue(hasattr(car1, "updated_at"))
        self.assertIsInstance(car1.id, str)
        self.assertIsInstance(car1.created_at, datetime)
        self.assertIsInstance(car1.updated_at, datetime)
        self.assertIsInstance(car1.name, str)
        self.assertIsInstance(car1.rent_price, int)
        self.assertIsInstance(car1.status, str)
        self.assertIsInstance(car1.fuel, str)

    def test_instant(self):
        """testing instantiation"""

        car2 = Car()
        self.assertEqual(car2.name, None)
        self.assertIsInstance(car2, Car)
        self.assertTrue(issubclass(Car, BaseModel))

    def test_to_dict(self):
        """ testing to_dict method """
        car3 = Car()
        car3.name = "audi"
        car3.rent_price = 120
        car3.status = "unbooked"
        car3.fuel = "Diesel"
        cr = car3.created_at
        up = car3.updated_at

        car_dict = car3.to_dict()
        self.assertEqual(type(car_dict), dict)
        self.assertIn("__class__", car_dict)
        self.assertEqual(car_dict['__class__'], 'Car')
        self.assertEqual(cr.isoformat(), car3.to_dict()["created_at"])
        self.assertEqual(up.isoformat(), car3.to_dict()["updated_at"])
        self.assertEqual(car_dict["name"], "audi")
        self.assertEqual(car_dict["fuel"], "Diesel")
        self.assertEqual(car_dict["rent_price"], 120)
        self.assertEqual(car_dict["status"], "unbooked")

        self.assertFalse("_sa_instance_state" in car_dict)

    @mock.patch('models.storage')
    def test_save(self, mock_storage):
        """ testing save method """
        car4 = Car()
        old_cr = car4.created_at
        old_up = car4.updated_at

        car4.save()

        new_cr = car4.created_at
        new_up = car4.updated_at

        self.assertNotEqual(old_up, new_up)
        self.assertEqual(old_cr, new_cr)
        self.assertTrue(mock_storage.new.called)
        self.assertTrue(mock_storage.save.called)
