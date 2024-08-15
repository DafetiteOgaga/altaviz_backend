from django.db import models
from django.conf import settings
from app_inventory.models import *
from django.db.models import F

# Create your models here.
class Post_Part(models.Model):
	name = models.ForeignKey(Part, on_delete=models.PROTECT, related_name="post_parts")
	quantity_posted = models.IntegerField()
	# total_quantity = models.IntegerField()
	other_info = models.CharField(max_length=1000)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
	posted_at = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		if self.pk is None:  # Only add quantity on first save
			self.name.total_quantity = F('total_quantity') + self.quantity_posted
			self.name.save(update_fields=["total_quantity"])
		super().save(*args, **kwargs)

class Post_Component(models.Model):
	name = models.ForeignKey(Component, on_delete=models.PROTECT, related_name="post_components")
	quantity_posted = models.IntegerField()
	# total_quantity = models.IntegerField()
	other_info = models.CharField(max_length=1000)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
	posted_at = models.DateTimeField(auto_now_add=True)
	# resolved_at = models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		if self.pk is None:  # Only add quantity on first save
			self.name.total_quantity = F('total_quantity') + self.quantity_posted
			self.name.save(update_fields=["total_quantity"])
		super().save(*args, **kwargs)

class Request_Part(models.Model):
	name = models.ForeignKey(Part, on_delete=models.PROTECT, related_name="request_parts")
	quantity_requested = models.IntegerField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
	requested_at = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		if self.pk is None:  # Only subtract quantity on first save
			self.name.total_quantity = F('total_quantity') - self.quantity_requested
			self.name.save(update_fields=["total_quantity"])
		super().save(*args, **kwargs)

class Request_Component(models.Model):
	name = models.ForeignKey(Component, on_delete=models.PROTECT, related_name="request_components")
	quantity_requested = models.IntegerField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
	requested_at = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		if self.pk is None:  # Only subtract quantity on first save
			self.name.total_quantity = F('total_quantity') - self.quantity_requested
			self.name.save(update_fields=["total_quantity"])
		super().save(*args, **kwargs)