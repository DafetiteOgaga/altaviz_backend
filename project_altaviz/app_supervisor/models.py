from django.db import models
from django.conf import settings

# Create your models here.
class Supervisor(models.Model):
    engineer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    is_deleted = models.BooleanField(default=False)

    def delete(self):
        self.is_deleted = True
        self.save()