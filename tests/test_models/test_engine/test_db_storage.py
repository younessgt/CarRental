#!/usr/bin/python3
"""
contain the Dbstorage class
"""

from models.car import Car
import unittest
from unittest import mock
from unittest.mock import patch, Mock
from models.engine import db_storage
Dbstorage = db_storage.Dbstorage


class TestDbstorage(unittest.TestCase):

    @patch('models.engine.db_storage.create_engine')
    @patch('models.engine.db_storage.getenv')
    def setUp(self, mock_getenv, mock_create_engine):
        """Set up test environment before each test"""
        mock_getenv.side_effect = ['user', 'password', 'host', 'db', 'test']
        mock_create_engine.return_value = Mock()
        self.db = Dbstorage()

    def test_init(self):
        """ test_init  method"""
        self.assertIsNotNone(self.db._Dbstorage__engine)

    @patch('models.engine.db_storage.Base.metadata')
    def test_reload(self, mock_metadata):
        """test reload method"""
        self.db.reload()
        mock_metadata.create_all.assert_called_once()
        self.assertIsNotNone(self.db._Dbstorage__session)

    def test_new(self):
        """test new method"""
        with patch('models.engine.db_storage.scoped_session') as mock_session:
            self.db.reload()
            mock_obj = Mock()
            self.db.new(mock_obj)
            mock_session.return_value.add.assert_called_with(mock_obj)

    def test_close(self):
        """test close method"""
        with patch('models.engine.db_storage.scoped_session') as mock_session:
            self.db.reload()
            self.db.close()
            mock_session.return_value.remove.assert_called_once()

    @patch('models.storage')
    def test_get(self, mock_storage):
        "test get method"
        car1 = Car(name="CC", fuel="Gaso", rent_price=75, status="unbooked")
        car1.save()
        mock_storage.get.return_value = car1
        get_instance = mock_storage.get(Car, car1.id)
        self.assertEqual(get_instance, car1)

    def test_save(self):
        """test save method"""
        with patch('models.engine.db_storage.scoped_session') as mock_session:
            self.db.reload()
            self.db.save()
            mock_session.return_value.commit.assert_called_once()
