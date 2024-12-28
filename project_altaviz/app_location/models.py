from django.db import models
from app_bank.models import State, Bank

# Create your models here.
class Location(models.Model):
	location = models.CharField(max_length=200, null=True, blank=True)
	# location2 = models.CharField(max_length=200, unique=True, null=True, blank=True)
	bank = models.ManyToManyField(Bank, related_name='banklocations', blank=True)
	state = models.ForeignKey(State, on_delete=models.PROTECT, related_name='statelocations', null=True, blank=True)
	region = models.ForeignKey('app_users.Region', on_delete=models.PROTECT, related_name='regionlocations', null=True, blank=True)
	class Meta:
		ordering = ['id']
	def __str__(self) -> str:
		return f'{self.location}.locationObj for {[bank.name for bank in self.bank.all()] if self.bank else None} in {self.state.name if self.state else None}'

