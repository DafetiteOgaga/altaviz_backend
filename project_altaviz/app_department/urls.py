from django.urls import path
from . import views

app_name = "app_department"

urlpatterns = [
	# Create your urlpatterns here.
	path('departments/', view=views.departments, name='department'),
]
