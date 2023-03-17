from django.db import models

# Create your models here.


class House(models.Model):
    category = models.CharField(max_length=32)
    barrio = models.CharField(max_length=200)
    departamento = models.CharField(max_length=200)
    square_meters = models.FloatField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    price = models.IntegerField()
    currency = models.CharField(max_length=16)
    full_link = models.CharField(max_length=200)
