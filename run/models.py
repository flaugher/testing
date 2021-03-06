from pdb import set_trace as debug
from django.db import models

"""
Each author publishes one or more books.
Each book has one and only one author.
Each author publishes with one or more publishers.
Each publisher publishes one or more authors.
"""
class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'author'


class Genre(models.Model):
    """
    A lookup table of book genres.
    """
    genre = models.CharField(max_length=50)

    def __str__(self):
        return self.genre

    class Meta:
        db_table = 'genre'

    @staticmethod
    def read_genre(genre_name):
        try:
            genre_inst = Genre.objects.get(genre=genre_name)
        except Genre.DoesNotExist:
            #msg = "Genre '%s' doesn't exist" % (genre_name)
            #logger.error(msg, exc_info=True)
            return None
        else:
            return genre_inst

class Book(models.Model):
    title = models.CharField(max_length=100)
    # Assigning related_name to FK allows you to do this:
    # a = Author.objects.create(name='Henry Miller')
    # a.books.create(name='Time of the Assassins')
    author = models.ForeignKey(Author, related_name='books')
    genre =  models.ForeignKey(Genre, related_name='genres')

    def __str__(self):
        return self.title

    def retrieve_isbn(self):
        return 'abc123'

    class Meta:
        db_table = 'book'


class Publisher(models.Model):
    """
    a = Author(name='author_name')
    a.save()
    p = Publisher(house='house_name')
    p.save()
    p.authors.add(a)
    """
    house = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)

    def __str__(self):
        return self.house

    class Meta:
        db_table = 'publisher'


class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)

    def __str__(self):
        return '%s %s' % (self.make, self.model)

    class Meta:
        db_table = 'car'

    def sound(self):
        return "vrooom!"


class Dealer(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % self.name

    def num_of_cars(self):
        return 100

    class Meta:
        db_table = 'dealer'
