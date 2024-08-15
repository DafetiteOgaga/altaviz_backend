from django.db import models

# Create your models here.
class Component(models.Model):
    name = models.CharField(max_length=100)
    total_quantity = models.IntegerField(default=0)

class Part(models.Model):
    name = models.CharField(max_length=100)
    total_quantity = models.IntegerField(default=0)
