from django.db import models

# Create your models here.
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Reservation(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)
    guest_count = models.IntegerField(default=0)
    comments = models.TextField(blank=True)