import mock
import pdb
import unittest
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from django_webtest import WebTest
from . import views
from .models import Car

# Run tests:
# cd ~/code/django/testing
# pm test run.tests

class TestViews(TestCase):
    # Tests that use Django TestCase
    def setUp(self):
        pass

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
        #pdb.set_trace()
        self.assertEqual(resp.status_int, 200)

# See https://matthewdaly.co.uk/blog/2015/08/02/testing-django-views-in-isolation/
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


class TestModels(unittest.TestCase):
    # howto: test model with mock (most basic test)
    def test_car_str(self):
        mock_car = mock.Mock(spec=Car)
        mock_car.make = "Honda"
        mock_car.model = "Civic"
        # howto: test mock model methods
        self.assertEqual(Car.__str__(mock_car), "Honda Civic")
        self.assertEqual(Car.sound(mock_car), "vrooom!")
