from django.db import models
# from app_users.models import Region

# Create your models here.
class Bank(models.Model):
    name = models.CharField(max_length=50, unique=True)
    states = models.ManyToManyField('State', related_name='banksList')
    class Meta:
        ordering = ['id']
    def __str__(self) -> str:
        return f'{self.name}.bankObj in {[state.name for state in self.states.all()]}'

class State(models.Model):
    name = models.CharField(max_length=50)
    initial = models.CharField(max_length=5, null=True, blank=True)
    region = models.ForeignKey('app_users.Region', on_delete=models.PROTECT, related_name='regionstates', null=True, blank=True)
    class Meta:
        ordering = ['id']
    def __str__(self) -> str:
        return f'{self.name}: {self.initial}'
