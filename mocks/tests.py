from datetime import datetime, timedelta
import mock
import unittest
from unittest.mock import MagicMock as MM
from .models import Car, get_max_items, get_first_name, get_full_name, get_car_make, get_car_wheels
from .classes import Book

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

    # patch "hijacks" the call to get_first_name and returns a MagicMock object.
    # mock_get_first_name is a MagicMock instance that corresponds to the get_first_name
    # function.
    @mock.patch('mocks.models.get_first_name')
    def test_function(self, mock_get_first_name):
        # howto: mock a function
        # This shows how to mock the return value for a function.  You
        # could call the function directly or override whatever it would
        # normally kind of like how you can override factoryboy instances.
        mock_get_first_name.return_value = 'Bob'  # Override default
        self.assertEquals(get_full_name('Robert'), 'Bob Flaugher')

    @mock.patch('mocks.models.Car.get_make')
    def test_method(self, mock_get_make):
        # howto: mock a class method
        # This just mocks what an instance method on a class would return
        mock_get_make.return_value = 'BMW'
        # We'll just throw in a test to check it
        self.assertEquals(get_car_make(), 'BMW')

    @mock.patch('mocks.models.Car.wheels', new_callable=mock.PropertyMock)
    def test_property(self, mock_wheels):
        # howto: mock a class property
        mock_wheels.return_value = 2
        # Normally, get_car_wheels returns 4.  Here we're confirming that
        # our mock makes it return 2 instead.
        self.assertEquals(get_car_wheels(), 2)

    @mock.patch('mocks.models.Car')
    def test_class(self, mock_car):
        # howto: mock (swap out) an entire class
        class NewCar(object):

            def get_make(self):
                return 'Audi'

            @property
            def wheels(self):
                return 6

        # key it make return_value an instance of the new class
        # This has the effect of intercepting calls to the Car class.
        # However, the only things that are changed in the Car class is
        # what's specified in the definition above.  get_car_make instantiates
        # a car instance and then calls get_make.  But we've mocked get_make
        # above so the function now returns 'Audi'.
        mock_car.return_value = NewCar()
        self.assertEquals(get_car_make(), 'Audi')
        self.assertEquals(get_car_wheels(), 6)

    @mock.patch('mocks.models.Car.for_make')
    def test_classmethod(self, mock_for_make):
        # howto: mock a classmethod
        # Same as mocking a method.
        mock_for_make.return_value = 'Lexus'
        # ...

    @mock.patch('mocks.models.Car.roll_call')
    def test_staticmethod(self, mock_get_roll_call):
        # howto: mock a staticmethod
        # Same as mocking a class method
        mock_get_roll_call.return_value = [Car('Ford')]
        # ...

    def test_return_value(self):
        # howto: mock a method's return value
        book = Book('Python 3')
        expected = datetime.today().strftime('%Y-%m-%d')
        actual = book.pub_date()
        self.assertEqual(actual, expected)

        # Now mock the return value to be yesterday
        book = Book('Python 3')
        tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        book.pub_date = MM(return_value=tomorrow)
        mock_expected = tomorrow
        actual = book.pub_date()
        #print("mock expected: " + mock_expected)
        #print("actual: " + actual)
        self.assertEqual(actual, mock_expected)
