import mock
import unittest
from .models import get_max_items, get_first_name, get_full_name

class TestMocks(unittest.TestCase):

    @mock.patch('mocks.models.MAX_ITEMS', 5)
    def test_constant(self):
        # howto: mock a constant
        # MAX_ITEMS = 10 but we're changing it to 5
        # You wouldn't actually test a constant like this.  This just
        # shows you could mock an external constant.
        self.assertEquals(get_max_items(), 5)

    def test_empty_first_name(self):
        self.assertEquals(get_first_name(''), 'Robert')

    def test_custom_first_name(self):
        self.assertEquals(get_first_name('Bob'), 'Bob')

    def test_get_full_name(self):
        self.assertEquals(get_full_name('Robert'), 'Robert Flaugher')

    @mock.patch('mocks.models.get_first_name')
    def test_get_first_name(self, mock_get_first_name):
        # howto: mock a function
        # This shows how to mock the return value for a function.  You
        # could call the function directly or override whatever it would
        # normally kind of like how you can override factoryboy instances.
        mock_get_first_name.return_value = 'Bob'
        self.assertEquals(get_full_name('Robert'), 'Bob Flaugher')



