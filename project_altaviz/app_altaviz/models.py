from django.db import models

# Create your models here.
class Home(models.Model):
	test = models.CharField(max_length=100)
	class Meta:
		ordering = ['id']
