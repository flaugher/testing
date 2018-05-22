import logging
logger = logging.getLogger(__name__)
from pdb import set_trace as debug

from .models import Car
from .classes import SimpleClass


def send_login_email():
    """Example of a function that sends an email."""
    from django.core.mail import send_mail
    send_mail()

def use_simple_class():
    inst = SimpleClass()
    result = inst.explode()
    #print(result)
    return(result)

def function():
    return "You have called function!"

def side_effect_function():
    return "You've called the side effect function!"

def logger_function():
     msg = 'Written by test_logger_function'
     logger.info(msg)

def get_car(id):
    """Get car by ID."""
    try:
        c = Car.objects.get(pk=id)
    except Car.DoesNotExist:
        return None
    return c
