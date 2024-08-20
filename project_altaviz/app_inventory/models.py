from django.db import models
from django.db.models import F

# Create your models here.
class ComponentName(models.Model):
	name = models.CharField(max_length=100, unique=True)
	date_created = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.name

class Component(models.Model):
	name = models.ForeignKey('ComponentName', on_delete=models.PROTECT, related_name='componentnames')
	quantity = models.IntegerField(default=0)
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
	def __str__(self):
		return self.name
	
class Part(models.Model):
	name = models.ForeignKey('PartName', on_delete=models.PROTECT, related_name='partnames')
	quantity = models.IntegerField(default=0)
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
