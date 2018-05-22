
class SimpleClass(object):

    def explode(self):
        return "kaboom!"

    @classmethod
    def yell(cls):
        return "fuck you!"


class Exceptioner(object):

    def raise_exc(self):
        """
        Raise an exception.
        """
        raise ValueError


class Class1(object):
    pass

    def __str__(self):
        return "I am class 1!"


class Class2(object):
    pass

    def __str__(self):
        return "I am class 2!"
