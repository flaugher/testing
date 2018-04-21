from django.db import models

class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)

    def __str__(self):
        return '%s %s' % (self.make, self.model)

    def sound(self):
        return "vrooom!"

