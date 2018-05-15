from django.db import models

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
