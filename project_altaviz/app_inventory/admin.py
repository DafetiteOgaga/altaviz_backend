from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ComponentName)
admin.site.register(Component)
admin.site.register(PartName)
admin.site.register(Part)
admin.site.register(RequestComponent)
admin.site.register(RequestPart)
admin.site.register(UnconfirmedPart)