from django.db import models

MAX_ITEMS = 10

def get_max_items():
    return MAX_ITEMS

def get_first_name(arg):
    return arg or "Robert"

def get_full_name(arg):
    return ' '.join((get_first_name(arg), 'Flaugher'))
