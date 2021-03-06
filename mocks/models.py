from contextlib import contextmanager
from django.db import models

MAX_ITEMS = 10

def get_max_items():
    return MAX_ITEMS

def get_first_name(arg):
    return arg or "Robert"

def get_full_name(arg):
    return ' '.join((get_first_name(arg), 'Flaugher'))

def get_car_make(make=None):
    # Kind of twisted logic but oh well
    car = Car()
    if make:
        car = Car.for_make(make)
    return car.get_make()

def get_car_wheels():
    # howto: read a property from a class
    return Car().wheels

class Car(object):

    def __init__(self, make=None):
        self.make = make
        self.closed = False

    @classmethod
    def for_make(cls, make):
        car = cls()
        car.make = make
        return car

    def get_make(self):
        return self.make

    @property
    def wheels(self):
        return 4

    @staticmethod
    def roll_call():
        return[Car('Ford'), Car('Chevy'), Car('BMw'), Car('Audi')]

    def close(self):
        self.closed = True

    def __repr__(self):
        return '<Car: %s>' % self.make

    def __eq__(self, other):
        return self.make == other.make

@contextmanager
def open_car(car):
    yield car
    car.close()

