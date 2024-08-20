from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(PostPart)
admin.site.register(PostComponent)
admin.site.register(RequestPart)
admin.site.register(RequestComponent)