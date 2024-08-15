from django.db import models
from app_engineer.models import Engineer
from app_supervisor.models import Supervisor
from app_help_desk.models import Help_Desk
from app_bank.models import Bank

# Create your models here.
class Fault(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    atm_number = models.IntegerField()
    # priority = models.IntegerField()
    status = models.BooleanField(default=False)
    confirm_resolve = models.BooleanField(default=False)
    verify_resolve = models.BooleanField(default=False)

    assigned_to = models.ForeignKey(Engineer, on_delete=models.PROTECT, related_name='assignedTo')
    supervised_by = models.ForeignKey(Supervisor, on_delete=models.PROTECT, related_name='supervisedBy')
    managed_by = models.ForeignKey(Help_Desk, on_delete=models.PROTECT, related_name='managedBy')
    logged_by = models.ForeignKey(Bank, on_delete=models.PROTECT, related_name='loggedBy')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(auto_now=True)
