from datetime import datetime

# The mocks you create against this class could just as easily be created
# against Django models.

class Book:

    def __init__(self, title):
        self.title = title

    def pub_date(self):
        return datetime.today().strftime('%Y-%m-%d')
