# Testing

This is where I keep scripts that demonstrate how to test my code.

When I last worked on this, I was trying to practice new testing techniques on Django's introductory
tutorial.  I had gotten to this page: [Django Tutorial, pt. 2](https://docs.djangoproject.com/en/1.11/intro/tutorial02/)

Also see ~/info/testing/README.md,  ~/info/django2/django_testing.md


#### Requirements

- Django > 1.11
- django-test-without-migrations
- mock
- coverage

#### Run tests

Execute run/tests.py: 
python manage.py test run.tests

Execute webtest/tests.py: 
python webtest/tests.py

Execute all tests: 
python manage.py test

#### Notes

Use profile.models:add_address and add_address_for as a way to implement
testable methods?

