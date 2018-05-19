import logging
logger = logging.getLogger(__name__)
from pdb import set_trace as debug

from .models import Car


def function():
    return "You have called function!"

def side_effect_function():
    return "Fuck all y'all!"

def logger_function():
     msg = 'Written by test_logger_function'
     logger.info(msg)

def get_car(id):
    """Get car by ID."""
    try:
        Car.objects.get(pk=id)
    except Car.DoesNotExist:
        #return True
        return None
    #return False
    return id
