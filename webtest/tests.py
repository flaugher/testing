from webtest import TestApp
from functions import application

# How to use WebTest

# Create some function to be tested, for example function.application

# Wrap it into a TestApp
app = TestApp(application)

# Get the response of an HTTP GET
resp = app.get('/')

# Run the test:
# cd ~/code/django/mytests
# python webtest/tests.py

# Check the results
assert resp.status == '200 OK'
assert resp.status_int == 200
assert resp.content_type == 'text/html'
assert resp.content_length > 0
resp.mustcontain('<html>')
