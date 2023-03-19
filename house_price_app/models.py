from django.db import models


class House(models.Model):
    id = models.IntegerField(primary_key=True)
    category = models.CharField(max_length=32)
    barrio = models.CharField(max_length=200)
    departamento = models.CharField(max_length=200)
    square_meters = models.CharField(max_length=32)
    bedrooms = models.CharField(max_length=32)
    bathrooms = models.CharField(max_length=32)
    price = models.IntegerField()
    currency = models.CharField(max_length=16)
    full_link = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.category} - {self.departamento} - {self.barrio} - {self.square_meters} sqm - {self.bedrooms} bed(s) - {self.bathrooms} bath(s) - {self.currency} {self.price} - {self.full_link}"
