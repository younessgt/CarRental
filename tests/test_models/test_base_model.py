#!/usr/bin/python3
""" Testing BaseModel Class """

import unittest
import models
from models.base_model import BaseModel
from datetime import datetime
from unittest import mock


class TestBaseModel(unittest.TestCase):
    """ Testing BaseModel Class """

    def test_attr(self):
        """ testing attributes"""
        model = BaseModel()
        model.name = "model"

        self.assertTrue(hasattr(model, "name"))
        self.assertTrue(hasattr(model, "id"))
        self.assertEqual(str, type(model.id))
        self.assertEqual(str, type(model.name))
        self.assertTrue(datetime, type(model.created_at))
        self.assertTrue(datetime, type(model.updated_at))
        self.assertEqual(len(model.__dict__), 4)

    def test_instantiation(self):
        """ testing if model is an instance of BaseModel """

        model1 = BaseModel()
        self.assertIsInstance(model1, BaseModel)

    def test_str(self):

        """ test cases for the object representation"""

        model2 = BaseModel()

        representation = "[BaseModel] ({}) {}".format(model2.id, model2.__dict__)
        self.assertEqual(representation, str(model2))

    def test_to_dict(self):
        """ testing to_dict method """

        model3 = BaseModel()
        model3.name = "test"
        cr = model3.created_at
        up = model3.updated_at

        model_dict = model3.to_dict()
        self.assertEqual(type(model_dict), dict)
        self.assertIn("__class__", model_dict)
        self.assertEqual(model_dict['__class__'], 'BaseModel')
        self.assertEqual(cr.isoformat(), model3.to_dict()["created_at"])
        self.assertEqual(up.isoformat(), model3.to_dict()["updated_at"])
        self.assertEqual(model_dict["name"], "test")

    @mock.patch('models.storage')
    def test_save(self, mock_storage):
        """ testing save method """
        model4 = BaseModel()
        old_cr = model4.created_at
        old_up = model4.updated_at

        model4.save()

        new_cr = model4.created_at
        new_up = model4.updated_at

        self.assertNotEqual(old_up, new_up)
        self.assertEqual(old_cr, new_cr)
        self.assertTrue(mock_storage.new.called)
        self.assertTrue(mock_storage.save.called)

    @mock.patch('models.storage')
    def test_update(self, mock_storage):
        """ testing update method """
        model5 = BaseModel()
        old_cr = model5.created_at
        old_up = model5.updated_at

        model5.save()

        new_cr = model5.created_at
        new_up = model5.updated_at

        self.assertNotEqual(old_up, new_up)
        self.assertEqual(old_cr, new_cr)
        self.assertTrue(mock_storage.save.called)
