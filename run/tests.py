import mock
import pdb
from pdb import set_trace as debug
import unittest
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from django.utils import six
from django_webtest import WebTest
from . import views
from .models import Car

# Run tests:
# cd ~/code/django/testing
# pm test run.tests

class TestViews(TestCase):

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
