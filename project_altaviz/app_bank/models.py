from django.db import models

# Create your models here.
class Bank(models.Model):
    name = models.CharField(max_length=50)

class Custodian(models.Model):
    bank = models.ForeignKey('Bank', on_delete=models.PROTECT, related_name='custodians')
    state = models.CharField(max_length=50)
    branch = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True, blank=True)
    quantity_of_atm = models.IntegerField()
