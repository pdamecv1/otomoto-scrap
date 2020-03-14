from django.db import models

# Create your models here.
class Offer(models.Model):
    url = models.CharField(max_length=250)
    location = models.CharField(max_length=100, blank=True, default='')
    creation = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, default='')
    phone = models.CharField(max_length=100, blank=True, default='')
    image = models.ImageField()

    # Specification
    # TODO: move to a different table?
    make = models.CharField(max_length=100, blank=True, default='')
    model = models.CharField(max_length=100, blank=True, default='')
    offer_from = models.CharField(max_length=100, blank=True, default='')
    category = models.CharField(max_length=100, blank=True, default='')
    production_year = models.IntegerField(blank=True, null=True)
    mileage = models.IntegerField(blank=True, null=True)
    engine_capacity = models.IntegerField(blank=True, null=True)
    fuel_type = models.CharField(max_length=100, blank=True, default='')
    power = models.IntegerField(blank=True, null=True)
    gearbox = models.CharField(max_length=100, blank=True, default='')
    propulsion = models.CharField(max_length=100, blank=True, default='')
    car_type = models.CharField(max_length=100, blank=True, default='')
    doors = models.IntegerField(blank=True, null=True)
    seats = models.IntegerField(blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, default='')
    is_aso_serviced = models.BooleanField(default=False)
    is_registered_in_poland = models.BooleanField(default=False)

    class Meta:
        ordering = ['make']
