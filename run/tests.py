try:  # python3
    from unittest import mock
    from unittest.mock import patch
    from unittest.mock import MagicMock as MM
except ImportError as e:  # python 2
    import mock
    from mock import patch
import unittest
import pdb
from pdb import set_trace as debug

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from django.utils import six

from django_webtest import WebTest
from .models import Car, Dealer
from . import functions as func
from . import views
from . import classes as cls

# Run tests:
# cd ~/code/django/testing
# pm test run.tests

# Python assertions: https://docs.python.org/3/library/unittest.html#test-cases


class TestExcep(unittest.TestCase):

    @mock.patch('run.classes.Exceptioner.raise_exc')
    def test_mock_exc_raised(self, mock_func):
        # howto: mock an exception to check that it's raised
        # This tests to see if a ValueError exception is raised
        # when the raise_exc function/method is called.
        # Either of the next two statements works
        #mock_func.side_effect = ValueError
        mock_func = MM(side_effect=ValueError("ValueError was raised"))
        # howto: test that an exception was raised
        self.assertRaises(ValueError, mock_func)

    def test_real_exc_raised(self):
        # howto: test that an exception is raised (using context manager)
        c = cls.Exceptioner()
        with self.assertRaises(ValueError):
            c.raise_exc()

#    @unittest.skip('Demonstrate skipping')
#    def test_nothing(self):
#        # howto: skip a test using unittest decorator
#        self.fail("This shouldn't happen")

class TestClass(unittest.TestCase):

    #@mock.patch('run.classes.Class1', autospec=True)
    #def test_mock_magic(self, mock_class):
    def test_mock_magic(self):
        # howto: mock a magic method TBD
        # Test default str
        self.assertEqual(cls.Class1.__str__(self), "I am class 1!")

    @mock.patch('run.classes.Class2')
    @mock.patch('run.classes.Class1')
    def test_classes(self, mock_class1, mock_class2):
        # howto: mock more than one object
        # howto: show that mocked object was called
        cls.Class1()
        cls.Class2()
        #assert mock_class1 is cls.Class1
        #assert mock_class2 is cls.Class2
        #assert mock_class1.called
        #assert mock_class2.called
        self.assertIs(mock_class1, cls.Class1)
        self.assertIs(mock_class2, cls.Class2)
        self.assertTrue(mock_class1.called)
        self.assertTrue(mock_class2.called)


class TestFunc(unittest.TestCase):

    def test_logger_func(self):
        # howto: test logs were written to
        with self.assertLogs('run.functions', 'INFO'):  # Will run without args
            func.logger_function()

    def test_func_no_mock(self):
        # howto: test a function without mocks
        self.assertEqual(func.function(), "You have called function!")

    @mock.patch('run.functions.function')
    def test_func_with_mock(self, mock_func):
        # howto: mock the return value of a function
        #print(mock_func)   # mock_func is a MagicMock
        mock_func.return_value = "You have called a mocked function!"
        self.assertEqual(func.function(), "You have called a mocked function!")


class TestModel(unittest.TestCase):

    @mock.patch('django.contrib.auth.models.User', autospec=True)
    def test_user(self, mock_user):
        # howto: mock a user
        mock_user.username = 'robert'
        mock_user.email = 'robert@example.com'
        self.assertEqual(mock_user.username, 'robert')
        mock_user.get_username.return_value = 'bob'
        self.assertEqual(mock_user.get_username(), 'bob')

    def test_is_car(self):
        """
        howto: test creating (crud) an instance of a model

        full_clean() will detect whether or not the model instance is
        valid.  You should run this test on *all* models.
        """
        car = Car(make='Honda', model='Civic')
        self.assertTrue(isinstance(car, Car))
        # howto: test that an object is an instance of a class
        self.assertIsInstance(car, Car)
        self.assertEqual(Car.__str__(car), "Honda Civic")
        car.full_clean()

    def test_car_str(self):
        # howto: test model with mock (most basic test) without patch
        mock_car = mock.Mock(spec=Car)
        mock_car.make = "Honda"
        mock_car.model = "Civic"
        # howto: test mock model methods
        self.assertEqual(Car.__str__(mock_car), "Honda Civic")
        self.assertEqual(Car.sound(mock_car), "vrooom!")

    @mock.patch('run.models.Dealer', autospec=True)
    def test_dealer(self, mock_dealer):
        # howto: mock a model using patch decorator
        mock_dealer.name = "Santa Monica BMW"
        mock_dealer.city = "Santa Monica"
        mock_dealer.num_of_cars.return_value = 200


class TestView(TestCase):

    def test_change_locale_works(self):
        """POST sets 'locale' key in session.

        howto: test that a view does something.
        """
        locale = 'es-mx'
        # howto: use requestfactory to simulate a request with a session
        # Use RequestFactory until you learn how to mock a request/response
        request = RequestFactory().post(
            '/locale/', {'locale': locale})
        request.session = {}

        views.change_locale(request)

        self.assertEqual(request.session['locale'], locale)

    def test_get_view(self):
        # howto: test a get request
        factory = RequestFactory()
        request = factory.get('get')
        response = views.get_view(request)
        self.assertEqual(response.status_code, 200)

    def test_posargs_view(self):
        # howto: test view having positional arguments
        # Note that you should hardcode the template into the view, not
        # pass it via the urlpattern's url function.
        factory = RequestFactory()
        # I'm not sure there's a way to do a post using the reverse
        # if you have positional or keyword args.  All examples that use
        # reverse don't have these args.
        request = factory.post('user')
        # Pass positional args here
        response = views.posargs_view(request, 1, 'foo')
        self.assertEqual(response.status_code, 200)

    def test_kwargs_view(self):
        # howto: test view having keyword arguments
        factory = RequestFactory()
        request = factory.post('user')
        response = views.kwargs_view(request, uid=1, uname='foobar')
        self.assertEqual(response.status_code, 200)

    def test_post_view(self):
        factory = RequestFactory()
        form_data = {
            'data1': 'data 1',
            'data2': 'data 2',
        }
        # When POSTing a form, the data arrives in request.POST.
        request = factory.post('userpost', data=form_data)
        response = views.post_view(request, uid=1, uname='foobar')
        self.assertEqual(response.status_code, 200)

    def test_json_view(self):
        factory = RequestFactory()
        # If you should want to convert post data to JSON, do json_data = json.dumps(post_data)
        json_data = '{"lists":[{"list_id":2,"list_name":"Couples to meet","action":"add"},{"list_id":1,"list_name":"Couples we\'ve met","action":"remove"},{"list_id":0,"list_name":"Sexy couples","action":"create"}]}'
        # When POSTing JSON, the data arrives in request.body.
        request = factory.post('json_view', data=json_data, content_type='application/json')
        response = views.json_view(request, uid=1, uname='foobar')
        if six.PY3:
            response_content = str(response.content, encoding='utf8')
        self.assertJSONEqual(response_content, {"status": "200"})

    def test_view_needing_user_session(self):
        """
        # howto: test view needing user and session
        user = UserFactory()
        factory = RequestFactory()
        user_agent = 'Mozilla/5.0'
        request = factory.get(reverse('create-account'),
                              HTTP_USER_AGENT=user_agent)
        # howto: create a test session when using RequestFactory
        request.session = {'device_type': 'computer',
                           'screen_width': 800}
        request.user = user
        response = create_account(request, 'ext_home_page.html')
        self.assertEqual(response.status_code, 200)
        """
        pass


class TestViewsWebTest(WebTest):
    # Tests that use WebTest
    # howto: use webtest to test a view

    # CSRF tokens hard to construct with raw POSTs such as what you
    # are doing in the change_locale_post test.  See:
    # https://pypi.python.org/pypi/django-webtest
    csrf_checks = False

    def setUp(self):
        pass

    def test_index_get(self):
        resp = self.app.get(reverse('index'))
        self.assertEqual(resp.status_int, 200)
        self.assertContains(resp, 'Hello, world!')

    def test_change_locale_post(self):
        locale = 'es-mx'
        resp = self.app.post(reverse('locale'))
        self.assertEqual(resp.status_int, 200)


# howto: skip tests that are expected to fail
#class ExpectedFailureTestCase(unittest.TestCase):
#    @unittest.expectedFailure
#    def test_fail(self):
#        self.assertEqual(1, 0, "broken")


# howto: skip a class using unittest decorator
# See https://matthewdaly.co.uk/blog/2015/08/02/testing-django-views-in-isolation/
#@unittest.skip('Skip entire class')
#class SnippetCreateViewTest(TestCase):
#    """
#    Test the snippet create view
#    """
#    def setUp(self):
#        self.user = UserFactory()
#        self.factory = RequestFactory()
#    def test_get(self):
#        """
#        Test GET requests
#        """
#        request = self.factory.get(reverse('snippet_create'))
#        request.user = self.user
#        response = SnippetCreateView.as_view()(request)
#        self.assertEqual(response.status_code, 200)
#        self.assertEqual(response.context_data['user'], self.user)
#        self.assertEqual(response.context_data['request'], request)
