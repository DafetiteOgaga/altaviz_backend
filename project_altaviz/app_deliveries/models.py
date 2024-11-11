from django.db import models
from app_users.models import User
from django.db.models import F

# Create your models here.
# note: deliveries setup and db field still active in User model
class Deliveries(models.Model):
	user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='userdeliveries', null=True, blank=True)
	deliveries = models.IntegerField(default=0)
	class Meta:
		ordering = ['id']
	def save(self, *args, **kwargs):
		print(f'entering deliveries ##########')
		# for deliveries
		# Before performing any operation with F expressions, ensure deliveries is an actual integer.
		print(f'self: {self}')
		print(f'self.pk: {self.pk}')
		print(f'self.user: {self.user}')
		# print(f'self.deliveries: {self.deliveries}')
		print(f'type(self.deliveries): {type(self.deliveries)}')
		if self.pk and isinstance(self.deliveries, int) and self.deliveries > 0:
			print(f'updating deliveries by 1 point ##########')
			# getUser = self.user
			# print(f'for user: {getUser}')
			# if getUser:
			print(f'found user: {self.user.email}')
			# Update the deliveries point of the existing user
			self.deliveries = F('deliveries') + self.deliveries
			self.save(update_fields=["deliveries"])
			print(f'updated deliveries field: {self.deliveries}')
			# Reset deliveries on the current instance to avoid double counting on re-save
			# self.deliveries = 0
			print(f'deliveries point updated ########################################')
			return  # Prevent saving a new instance

		# If no existing deliveries, proceed with saving the new instance
		else:
			print(f'creating new user. deliveries default value used ##########')
			# Call the parent class's save method
			super().save(*args, **kwargs)
