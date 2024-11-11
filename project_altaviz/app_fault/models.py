from django.db import models
# from app_engineer.models import Engineer
# from app_supervisor.models import Supervisor
# from app_help_desk.models import HelpDesk
from app_custodian.models import Custodian
from app_inventory.models import Component, Part, RequestComponent, RequestPart
# from app_requests.models import RequestComponent, RequestPart
from app_location.models import Location
from django.conf import settings

# Create your models here.
class FaultName(models.Model):
	name = models.CharField(max_length=100)
	class Meta:
		ordering = ['id']
	def __str__(self) -> str:
		return self.name

class Fault(models.Model):
	title = models.ForeignKey('FaultName', on_delete=models.PROTECT, related_name='faults', null=True, blank=True)
	other = models.TextField(null=True, blank=True)

	confirm_resolve = models.BooleanField(default=False)
	confirmed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='confirmedby', blank=True, null=True)
	verify_resolve = models.BooleanField(default=False)

	replacement_engineer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='verifiedby', blank=True, null=True)

	location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='faultlocation', null=True, blank=True)
	assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='assignedto', null=True, blank=True)
	supervised_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='supervisedby', null=True, blank=True)
	managed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='managedby', null=True, blank=True)
	logged_by = models.ForeignKey(Custodian, on_delete=models.PROTECT, related_name='loggedby', null=True, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	resolved_at = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['id']
