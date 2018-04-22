import mock
import pdb
import unittest
from datetime import datetime, date, time
from django.test import TestCase
from django.utils import timezone
from . import views

class TestModels(unittest.TestCase):
    pass

class TestViews(unittest.TestCase):
    # howto: test the simplest view with a mock request instance
    def test_index(self):
        mock_request = mock.Mock()
        mock_request.session = {}
        response = views.index(mock_request)
        self.assertEqual(response.status_code, 200)
