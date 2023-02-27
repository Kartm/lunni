from django.db import models

class Person(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=255)
    #
    # date
    # description
    # category
    # amount