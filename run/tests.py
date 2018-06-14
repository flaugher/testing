try:  # python3
    from unittest import mock
    from unittest.mock import patch
    from unittest.mock import MagicMock
    from unittest.mock import MagicMock as MM
except ImportError as e:  # python 2
    import mock
    from mock import patch
import unittest
import pdb
from pdb import set_trace as debug
import requests

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from django.utils import six

from django_webtest import WebTest
from mock_django import ModelMock

from .factories import *
from .models import Car, Dealer, Author, Book, Publisher, Genre
from . import functions as func
from . import views
from . import classes as cls

# Run tests:
# cd ~/code/django/testing
# pm test run.tests

# Python assertions: https://docs.python.org/3/library/unittest.html#test-cases


class TestModel(unittest.TestCase):

    def test_many_to_many_factory(self):
        """
        howto: create factory for table containing a many-to-many (manytomany) relationship.
        """
        publisher = PublisherFactory(house='Harper Collins')
        author = AuthorFactory(name='Henry Thoreau')
        publisher.authors.add(author)
        self.assertIsInstance(publisher, Publisher)
        # If you debug here and query the test_testing database, you'd
        # see the publisher and author records with a linking table entry
        # that links the two tables.

    def test_lookup_table_pass(self):
        """
        howto: test a lookup table without using mocks
        Note that the lookup table is populated by a migration file
        which is run before the test is executed.
        """
        genre_name = 'history'
        genre_inst = Genre.read_genre(genre_name)
        self.assertIsInstance(genre_inst, Genre)
        self.assertEqual(genre_inst.genre, genre_name)

    def test_lookup_table_fail(self):
        """
        A failing version of test_lookup_table
        """
        genre_name = 'fantasy'
        genre_inst = Genre.read_genre(genre_name)
        self.assertIsNone(genre_inst, Genre)
        self.assertRaises(Genre.DoesNotExist)

    def test_mock_lookup_table(self):
        """
        howto: mock a lookup table using mock-django library
        """
        mock_genre = ModelMock(Genre)   # Genre is a lookup table
        mock_genre.id = 1
        mock_genre.genre = 'Science Fiction'
        mock_author = MagicMock(spec=Author, autospec=True)
        mock_author.name = 'Henry Miller'
        # I shouldn't have to manually set _state.  Not sure why test
        # was failing if I didn't.
        mock_author._state = mock.Mock()
        b = Book(author=mock_author, genre=mock_genre, title='Time of the Assassins')
        self.assertIsInstance(b, Book)

    @mock.patch('django.contrib.auth.models.User', autospec=True)
    def test_mock_user(self, mock_user):
        """
        howto: test a mocked user
        """
        mock_user.username = 'robert'
        mock_user.email = 'robert@example.com'
        self.assertEqual(mock_user.username, 'robert')
        mock_user.get_username.return_value = 'bob'
        self.assertEqual(mock_user.get_username(), 'bob')

    @mock.patch('run.models.Car', autospec=True)
    def test_mock_model_instance(self, mock_car):
        """
        howto: test crud: create an instance of a model using a mock
        howto: mock a model's attributes
        """
        mock_car.make = "Honda"
        mock_car.model = "Civic"
        # howto: test mock model methods
        self.assertIsInstance(mock_car, Car)
        self.assertEqual(Car.__str__(mock_car), "Honda Civic")
        self.assertEqual(Car.sound(mock_car), "vrooom!")

    @mock.patch('run.models.Book', autospec=True)
    @mock.patch('run.models.Author', autospec=True)
    def test_mock_model_instance_with_fk(self, mock_author, mock_book):
        """
        howto: test a model instance having a foreign key (FK)
        """
        # independent instance
        mock_author.name = 'Henry Miller'
        # dependent FK instance
        mock_book.title = 'Time of the Assassins'
        mock_book.author = mock_author
        a = Author()
        b = Book()
        self.assertIsInstance(a, Author)
        self.assertIsInstance(b, Book)

    @mock.patch('run.models.Book.retrieve_isbn', autospec=True)
    def test_mock_model_method(self, mock_method):
        """
        howto: mock a model method
        """
        mock_method.return_value = 'foo123'
        isbn = Book().retrieve_isbn()
        self.assertEqual(isbn, 'foo123')


class TestView(TestCase):

    def test_get_view(self):
        # howto: test a get request
        factory = RequestFactory()
        request = factory.get('get')
        response = views.get_view(request)
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

    def test_mock_view_needing_user_session(self):
        """
        # howto: test a view requiring a user and session using a mock
        mock_request = mock.Mock()
        mock_request.user = mock.Mock()
        mock_request.user.is_superuser = mock.Mock()
        mock_request.user.is_superuser.return_value = True
        mock_request.session = {}
        ...
        response = some_view(mock_request)
        self.assertEqual(response.status_code, 200)

        This way is easier than using Request and User factories as shown next.
        """
        pass

    def test_view_needing_user_session(self):
        """
        # howto: test a view requiring a user and session using RequestFactory
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

    def test_change_locale_works(self):
        """
        howto: test that a view does something.

        POST sets 'locale' key in session.
        """
        locale = 'es-mx'
        # howto: use requestfactory to simulate a request with a session
        # Use RequestFactory until you learn how to mock a request/response
        request = RequestFactory().post(
            '/locale/', {'locale': locale})
        request.session = {}
        views.change_locale(request)
        self.assertEqual(request.session['locale'], locale)

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


class TestFunc(unittest.TestCase):

    def test_send_mail(self):
        """
        howto: send testing mail using monkey patching

        Note that you could also mock the send_mail function:
        @mock.patch('run.functions.send_login_email.send_mail')
        def fake_send_mail(self, mock_send_mail):
            ...
        """
        def fake_send_mail(subject='foo', body='baz', from_email='jeek', to_list='[]'):
            self.subject = subject
            self.body = body
            self.from_email = from_email
            self.send_mail_called = True

        self.send_mail_called = False
        # Replace Python's send_mail with your fake version and use the
        # latter for testing
        func.send_mail = fake_send_mail
        func.send_mail()
        self.assertTrue(self.send_mail_called)

    def test_logger(self):
        """
        howto: test logs were written to
        """
        with self.assertLogs('run.functions', 'INFO'):  # Will run without args
            func.logger_function()

    @mock.patch('run.functions.function')
    def test_func_with_mock(self, mock_func):
        """
        howto: mock the return value of a function
        """
        mock_func.return_value = "You have called a mocked function!"
        self.assertEqual(func.function(), "You have called a mocked function!")

    def test_func_without_mock(self):
        """
        howto: test a function without mocks
        """
        self.assertEqual(func.function(), "You have called function!")

    @mock.patch('run.functions.function')
    def test_func_with_side_effect(self, mock_func):
        """
        howto: mock a side effect
        """
        mock_func.side_effect = func.side_effect_function
        self.assertEqual(func.function(), "You've called the side effect function!")

    #@unittest.skip('')
    @mock.patch('run.functions.function')
    def test_use_function(self, mock_func):
        """
        Show that the function is being mocked
        """
        # Show mock
        #print(mock_func)
        # Show function has been mocked
        #print(func.function)
        # Show calling the function returns a mock
        # Here, we're calling the mock which returns a different mock.
        # Since MagicMock implements __call__, we can call a MM.
        # This is a child mock of the func.function() mock.
        # See http://bit.ly/2x4P7a5
        #print(func.function())
        self.assertIs(func.function, mock_func)
        self.assertIsNot(func.function, func.function())

    @unittest.skip('')
    #@unittest.expectedFailure
    @mock.patch('run.models.Car', autospec=True)
    def test_function_gets_object(self, mock_car):
        """
        howto: test a function that retrieves a model or class instance

        This is an integration test since it touches the database.
        """
        # Test exception
        id = 1
        mock_car.objects.get = mock.Mock(side_effect=Car.DoesNotExist)
        self.assertIsNone(func.get_car(id))
        # Test success
        c = Car(make="Honda", model="Civic")
        c.save()
        c = Car.objects.get(make="Honda", model="Civic")
        self.assertIsInstance(c, Car)
        self.assertEqual(c.make, "Honda")
        self.assertEqual(c.model, "Civic")


class TestClass(unittest.TestCase):

    # The @mock.patch decorator passes a MagicMock object that replaces
    # the class you are mocking into the function it is decorating.
    # The MM object is assigned to the argument 'mock_class'.
    @mock.patch('run.classes.SimpleClass', autospec=True)
    def test_mock_class(self, mock_class):
        """
        howto: test a mock class
        howto: test a mock class instance method
        """
        # Show the class has been replaced by the mock (ids are equal)
        #print(mock_class)
        #print(cls.SimpleClass)
        self.assertIs(mock_class, cls.SimpleClass)
        # Create an instance of the mocked SimpleClass
        inst = cls.SimpleClass()
        # Show calling the class results in a new mock
        #print(inst)

        # Show return value of mock instance is same as return value of class
        # Note that the return value of the inital mock you created is the
        # same as the mock 'inst' variable that was created when you instantiated
        # the mocked class.
        self.assertIs(inst, mock_class.return_value)
        # Now let's change the return value of explode which is an instance
        # method:
        mock_class.return_value.explode.return_value = 'ka-blooey!'
        # Note that in the command above, mock_class.return_value returns
        # the MM object that represents an instance of SimpleClass so
        # mock_class.return_value.explode returns a new MM object that
        # represents the explode method of that SimpleClass instance.
        # Therefore, mock_class.return_value.explode.return_value sets
        # The return value of the mocked explode method of that mocked
        # class instance.

        # Now continuing, create an instance of the mocked class
        inst = cls.SimpleClass()
        # Call the instance method
        result = inst.explode()
        #print(result)
        self.assertEqual(result, 'ka-blooey!')

    @mock.patch('run.classes.SimpleClass.yell')
    def test_mock_class_method(self, mock_class_method):
        """
        howto: mock a class method

        Note that you're not setting autospec=True.  Therefore, if
        you change yell by adding a parameter, this test will still
        pass.
        """
        mock_class_method.return_value = 'fuck you all to hell!'
        inst = cls.SimpleClass()
        result = inst.yell()
        self.assertEqual(result, 'fuck you all to hell!')

    def test_plain_class(self):
        """
        howto: test a class without mocks
        """
        self.assertEqual(func.use_simple_class(), "kaboom!")

    def test_class_string(self):
        # howto: test a class default string
        self.assertEqual(cls.Class1.__str__(self), "I am class 1!")

    @mock.patch('run.classes.Class2')
    @mock.patch('run.classes.Class1')
    def test_classes(self, mock_class1, mock_class2):
        # howto: mock more than one class object
        # howto: show that mocked class object was called
        cls.Class1()
        cls.Class2()
        self.assertIs(mock_class1, cls.Class1)
        self.assertIs(mock_class2, cls.Class2)
        self.assertTrue(mock_class1.called)
        self.assertTrue(mock_class2.called)


class TestApi(unittest.TestCase):

    def fetch_repo_names(url, username):
        """Fetch repo names.

        Called from test below.
        """
        repos = requests.get(url).json()
        return [repo['name'] for repo in repos]

    @mock.patch('requests.get')
    def test_mock_api(self, mock_get):
        """howto: mock an api.

        This test patches the requests.get function which is called by
        fetch_repo_names with a mock value.
        """
        mock_get.return_value.json.return_value = [
            {"name": "first"},
            {"name": "second"}]

        username = 'johndoe'
        url = ('https://api.github.com/users/{}'
               '/repos'.format(username))
        expected_names = ['first', 'second']
        returned_names = TestApi.fetch_repo_names(url, username)
        self.assertEqual(expected_names, returned_names)
        mock_get.assert_called_once_with(url)

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


class TestViewUsingWebTest(WebTest):
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
