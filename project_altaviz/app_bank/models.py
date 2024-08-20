from django.db import models
from django.conf import settings

# Create your models here.
class Bank(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.name

class Custodian(models.Model):
    email = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='mail')
    bank = models.ForeignKey('Bank', on_delete=models.PROTECT, related_name='bank')
    state = models.CharField(max_length=50)
    branch = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True, blank=True)
    # is_deleted = models.BooleanField(default=False)
    # def delete(self):
    #     self.is_deleted = True
    #     self.save()
    def __str__(self) -> str:
        return f'{self.state}, {self.branch}, {self.location}'
