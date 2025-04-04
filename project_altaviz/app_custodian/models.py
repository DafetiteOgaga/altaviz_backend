from django.db import models
from django.conf import settings
from app_bank.models import Bank, State
# from app_department.models import Department
from app_location.models import Location
from app_users.models import Engineer, Region, User

# Create your models here.
class Branch(models.Model):
	name = models.CharField(max_length=100)
	# custodian = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='branchcustodian', null=True, blank=True) # remove this field
	# custodian = models.ForeignKey('Custodian', on_delete=models.PROTECT, related_name='branchcustodian', null=True, blank=True)
	branch_engineer = models.ForeignKey(Engineer, on_delete=models.DO_NOTHING, related_name='branchengineer', null=True, blank=True)
	bank = models.ForeignKey(Bank, on_delete=models.PROTECT, related_name='bankbranches', null=True, blank=True)  # A bank can have multiple branches
	state = models.ForeignKey(State, on_delete=models.PROTECT, related_name='statebranches', null=True, blank=True)  # A state can have multiple branches
	location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='locationbranches', null=True, blank=True)  # A location can have multiple branches
	region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name='branchregion', null=True, blank=True)
	class Meta:
		ordering = ['id']
	def __str__(self) -> str:
		return f'{self.name}.branchObj for {self.bank.name if self.bank else "no bank yet"} in {self.location.location if self.location else "no location yet"} ({self.state.name if self.state else "no state yet"}): {self.id}'

class Custodian(models.Model):
	# custodian = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='custodiandata', null=True, blank=True)
	custodian = models.ForeignKey(User, on_delete=models.PROTECT, related_name='custodiandata', null=True, blank=True)
	branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='custodiansbranch', null=True, blank=True)
	class Meta:
		ordering = ['id']
	def __str__(self) -> str:
		return f'custodian {self.custodian.email} for {self.branch.name}'
