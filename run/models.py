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

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author)

    def __str__(self):
        return self.title

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

    def sound(self):
        return "vrooom!"

    class Meta:
        db_table = 'car'

class Dealer(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % self.name

    def num_of_cars(self):
        return 100

    class Meta:
        db_table = 'dealer'
