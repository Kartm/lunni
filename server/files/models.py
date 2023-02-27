from django.db import models


class Entry(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=255)
    account = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
