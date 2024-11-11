from django.db import models
from django.db.models import F
from django.conf import settings
# from app_fault.models import Fault

# Create your models here.
class ComponentName(models.Model):
	name = models.CharField(max_length=100, unique=True)
	date_created = models.DateTimeField(auto_now_add=True)
	class Meta:
		ordering = ['id']
	def __str__(self):
		return self.name

class Component(models.Model):
	name = models.ForeignKey('ComponentName', on_delete=models.PROTECT, related_name='componentnames')
	quantity = models.IntegerField(default=0)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
	class Meta:
		ordering = ['id']
	def save(self, *args, **kwargs):
		if not self.pk: # Check if a component with the same name exists
			existing_component = Component.objects.filter(name=self.name).first()
			if existing_component:
				# Update the quantity of the existing component
				existing_component.quantity = F('quantity') + self.quantity
				existing_component.save(update_fields=["quantity"])
				return  # Prevent saving a new instance

		# If no existing component, proceed with saving the new instance
		super().save(*args, **kwargs)
	def __str__(self) -> str:
		return f'{self.name}: {self.quantity}'

class PartName(models.Model):
	name = models.CharField(max_length=100, unique=True)
	date_created = models.DateTimeField(auto_now_add=True)
	class Meta:
		ordering = ['id']
	def __str__(self):
		return self.name

class Part(models.Model):
	name = models.ForeignKey('PartName', on_delete=models.PROTECT, related_name='partnames')
	quantity = models.IntegerField(default=0)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
	class Meta:
		ordering = ['id']
	def save(self, *args, **kwargs):
		if not self.pk: # Check if a component with the same name exists
			existing_part = Part.objects.filter(name=self.name).first()
			if existing_part:
				# Update the quantity of the existing component
				existing_part.quantity = F('quantity') + self.quantity
				existing_part.save(update_fields=["quantity"])
				return  # Prevent saving a new instance

		# If no existing component, proceed with saving the new instance
		super().save(*args, **kwargs)
	def __str__(self) -> str:
		return f'{self.name}: {self.quantity}'

class RequestPart(models.Model):
	name = models.ForeignKey(PartName, on_delete=models.PROTECT, related_name="requestparts")
	quantityRequested = models.IntegerField()
	fault = models.ForeignKey('app_fault.Fault', on_delete=models.SET_NULL, related_name='partfault', null=True, blank=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='partrequestuser')
	reason = models.TextField(blank=True, null=True)
	approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='partapprovedby', null=True, blank=True) # must be null/blank at creation
	approved = models.BooleanField(default=False)
	rejected = models.BooleanField(default=False)
	requested_at = models.DateTimeField(auto_now_add=True)
	approved_at = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['id']

class RequestComponent(models.Model):
	name = models.ForeignKey(ComponentName, on_delete=models.PROTECT, related_name="requestcomponents")
	quantityRequested = models.IntegerField()
	fault = models.ForeignKey('app_fault.Fault', on_delete=models.SET_NULL, related_name='componentfault', null=True, blank=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='componentrequestuser')
	reason = models.TextField(blank=True, null=True)
	approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='componentapprovedby', null=True, blank=True) # must be null/blank at creation
	approved = models.BooleanField(default=False)
	rejected = models.BooleanField(default=False)
	requested_at = models.DateTimeField(auto_now_add=True)
	approved_at = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['id']

class UnconfirmedPart(models.Model):
	name = models.CharField(max_length=100)
	quantity = models.IntegerField(default=0)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='partpostedby')
	# status = models.BooleanField(default=False)
	approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="approvedBy")
	approved = models.BooleanField(default=False)
	rejected = models.BooleanField(default=False)
	requested_at = models.DateTimeField(auto_now_add=True)
	approved_at = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['id']