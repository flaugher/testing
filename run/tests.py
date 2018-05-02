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

    def test_user_pos(self):
        # howto: test view having positional arguments
        # Note that you should hardcode the template into the view, not
        # pass it via the urlpattern's url function.
        factory = RequestFactory()
        # I'm not sure there's a way to do a post using the reverse
        # if you have positional or keyword args.  All examples that use
        # reverse don't have these args.
        request = factory.post('user/')
        #pdb.set_trace()
        # Pass positional args here
        response = views.user_pos(request, 1, 'foo')
        self.assertEqual(response.status_code, 200)

    def test_user_kw(self):
        # howto: test view having keyword arguments
        factory = RequestFactory()
        request = factory.post('user/')
        response = views.user_kw(request, uid=1, uname='foobar')
        self.assertEqual(response.status_code, 200)

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

    def test_post_form_to_view(self):
        """
        # howto: post a form to a view
        user = UserFactory()
        template = 'ext_home_page.html'
        factory = RequestFactory()
        # form fields passed via data parameter
        request = factory.post(reverse('create-account'),
                               {'username': 'testuser',
                                'password1': 'testpass1',
                                'password2': 'testpass2',
                                'user_type_cd': settings.COUPLE_CD},
                               HTTP_USER_AGENT=self.user_agent)
        request.user = user
        response = create_account(request, template)
        self.assertContains(response, 'Passwords must match')
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
