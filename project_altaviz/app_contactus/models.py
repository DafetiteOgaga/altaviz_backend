from django.db import models
from django.conf import settings

# Create your models here.
class ContactUs(models.Model):
	name = models.CharField(max_length=100, null=True, blank=True)
	email = models.EmailField(max_length=100, null=True, blank=True)
	message = models.TextField(max_length=1000)
	class Meta:
		ordering = ['id']

	def __str__(self) -> str:
		return self.email