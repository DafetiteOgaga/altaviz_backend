from django.urls import path
from . import views

urlpatterns = [
	# Create your urlpatterns here.
	path('', view=views.home, name='home'),
	path('nothing/', view=views.placeholder, name='placeholder'),
]
